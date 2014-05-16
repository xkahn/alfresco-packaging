DESTDIR=/
PWD=$(shell pwd)
MYDIR=$(shell basename ${PWD})
SPIN := 1
DATE := $(shell date +%Y%m%d)
TYPE := community
APPSERVER := tomcat7
VERSION ?= 4.2.f
RELEASE ?= $(DATE).$(SPIN)
VERREL := $(VERSION)-$(RELEASE)

TOMCAT_HOME=/usr/share/${APPSERVER}

deb: alfresco-${TYPE}-4.2.f.zip pkgdeb
rpm: pkgrpm

pkgdeb:

pkgrpm: alfresco-${TYPE}-${VERSION}.zip dist
	cp alfresco-${TYPE}-${APPSERVER}-${VERSION}.tar.gz support/alfresco-rebuild-amp support/alfresco-share-rebuild-amp support/alfresco support/alfresco.conf support/alfresco-ooo support/jk-workers.properties support/email-server.properties support/openoffice-document-formats.xml ~/rpmbuild/SOURCES/
	rpmbuild -ba alfresco-${TYPE}-${APPSERVER}.spec

alfresco-community-4.2.f.zip:
	wget http://dl.alfresco.com/release/community/4.2.f-build-00012/alfresco-community-4.2.f.zip

dist: distclean
	mkdir alfresco-${TYPE}-${APPSERVER}-${VERSION}
	(cd alfresco-${TYPE}-${APPSERVER}-${VERSION}; unzip ../alfresco-${TYPE}-${VERSION}.zip)
	mkdir alfresco-${TYPE}-${APPSERVER}-${VERSION}/extensions
	mkdir alfresco-${TYPE}-${APPSERVER}-${VERSION}/endorsed
	mkdir -p alfresco-${TYPE}-${APPSERVER}-${VERSION}/extras/databases/mysql
	mv alfresco-${TYPE}-${APPSERVER}-${VERSION}/web-server/shared/classes/alfresco/* alfresco-${TYPE}-${APPSERVER}-${VERSION}/extensions
	mv alfresco-${TYPE}-${APPSERVER}-${VERSION}/web-server/shared/classes/alfresco-global.properties.sample alfresco-${TYPE}-${APPSERVER}-${VERSION}/extensions/extension/alfresco-global.properties
	mv alfresco-${TYPE}-${APPSERVER}-${VERSION}/web-server/webapps/* alfresco-${TYPE}-${APPSERVER}-${VERSION}/
	mv alfresco-${TYPE}-${APPSERVER}-${VERSION}/web-server/lib/* alfresco-${TYPE}-${APPSERVER}-${VERSION}/endorsed
	rm -rf alfresco-${TYPE}-${APPSERVER}-${VERSION}/web-server 
	rm -rf alfresco-${TYPE}-${APPSERVER}-${VERSION}/bin/*.sh alfresco-${TYPE}-${APPSERVER}-${VERSION}/*.bat
	cp support/*.sql alfresco-${TYPE}-${APPSERVER}-${VERSION}/extras/databases/mysql
	cp Makefile alfresco-${TYPE}-${APPSERVER}-${VERSION}
	cp *.spec alfresco-${TYPE}-${APPSERVER}-${VERSION}
	mkdir -p WEB-INF/lib
	zip -m -r alfresco-${TYPE}-${APPSERVER}-${VERSION}/alfresco.war WEB-INF
	tar cfz alfresco-${TYPE}-${APPSERVER}-$(VERSION).tar.gz alfresco-${TYPE}-${APPSERVER}-$(VERSION) --exclude libmysqltcl.so --exclude libmysqltcl.dll --exclude Win32Utils.dll --exclude Win32Utilsx64.dll --exclude Win32NetBIOS.dll --exclude Win32NetBIOSx64.dll
	rm -rf alfresco-${TYPE}-${APPSERVER}-$(VERSION)

distclean:
	rm -rf alfresco-${TYPE}-${APPSERVER}-$(VERSION)

install:
	mkdir -p ${DESTDIR}/usr/share/doc/alfresco-${TYPE}-${VERSION}
	cp -a README.txt licenses ${DESTDIR}/usr/share/doc/alfresco-${TYPE}-${VERSION}
	mkdir -p ${DESTDIR}/usr/share/alfresco-${TYPE}
	cp -a endorsed extensions extras ${DESTDIR}/usr/share/alfresco-${TYPE}
	cp -a alfresco.war ${DESTDIR}/usr/share/alfresco-${TYPE}/alfresco-real.war
	cp -a share.war ${DESTDIR}/usr/share/alfresco-${TYPE}/share-real.war
	mkdir -p ${DESTDIR}/var/lib/alfresco/alf_data
	mkdir -p ${DESTDIR}/usr/share/alfresco-${TYPE}/amp.d
	mkdir -p ${DESTDIR}/usr/share/alfresco-${TYPE}/shareamp.d
	mkdir -p ${DESTDIR}/var/lib/${APPSERVER}/shared/classes
	mkdir -p ${DESTDIR}/usr/share/alfresco-${TYPE}/extensions/extension/license
	ln -sf /usr/share/alfresco-${TYPE}/extensions ${DESTDIR}/var/lib/${APPSERVER}/shared/classes/alfresco
	ln -sf /usr/share/${APPSERVER}/shared/classes/alfresco/extension/alfresco-global.properties ${DESTDIR}/var/lib/${APPSERVER}/shared/classes/alfresco-global.properties
	mkdir -p ${DESTDIR}/usr/share/${APPSERVER}
	ln -sf /var/lib/${APPSERVER}/shared ${DESTDIR}/usr/share/${APPSERVER}/shared

uninstall:
	rm -rf ${DESTDIR}/usr/share/alfresco
	rm -rf ${DESTDIR}/usr/share/doc/alfresco-${TYPE}-${VERSION}
