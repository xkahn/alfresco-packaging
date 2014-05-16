Name:		alfresco-community-tomcat7
Version:	4.2.f
Release:	1%{?dist}
Summary:	Alfresco Enterprise Content Management (ECM) Community Edition

Group:		Applications/Internet
License:	APL
URL:		http://wiki.alfresco.com/wiki/Community_file_list_4.2.f
Source0:	alfresco-community-tomcat7-4.2.f.tar.gz
Source2:        alfresco.conf
Source3:	jk-workers.properties
Source5:	alfresco-share-rebuild-amp
Source6:	alfresco-repo-rebuild-amp
BuildArch:      noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:	java >= 1.7.0, mysql, openoffice.org-base >= 3.0, openoffice.org-ure >= 3.0, openoffice.org-calc >= 3.0, openoffice.org-core >= 3.0, openoffice.org-draw >= 3.0, openoffice.org-graphicfilter >= 3.0, openoffice.org-impress >= 3.0, openoffice.org-math >= 3.0, openoffice.org-writer >= 3.0, openoffice.org-xsltfilter >= 3.0, openoffice.org-headless >= 3.0, ImageMagick >= 3.0, mysql-connector-java >= 3.0, swftools >= 0.9.0, httpd, mod_jk, xalan-j2, tomcat7
BuildRequires:  zip, unzip

Provides: alfresco, alfresco-community

%description
Alfresco is the Open Source Alternative for Enterprise Content Management (ECM), providing Document 
Management, Collaboration, Records Management, Knowledge Management, Web Content Management and Imaging.  
This package targets tomcat 5 with an Apache frontend using mod_jk

%prep
%setup -q


%build

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
%{__install} -p -D -m 644 %{SOURCE2} $RPM_BUILD_ROOT/etc/httpd/conf.d/alfresco.conf
%{__install} -p -D -m 644 %{SOURCE3} $RPM_BUILD_ROOT/etc/tomcat7/jk-workers.properties
%{__install} -p -D -m 755 bin/alfresco-mmt.jar $RPM_BUILD_ROOT/usr/share/alfresco-community/bin
%{__install} -p -D -m 755 %{SOURCE5} $RPM_BUILD_ROOT/usr/bin/alfresco-share-rebuild-amp
%{__install} -p -D -m 755 %{SOURCE6} $RPM_BUILD_ROOT/usr/bin/alfresco-repo-rebuild-amp

%clean
rm -rf $RPM_BUILD_ROOT


%post
# Build the Alfresco WAR file
/usr/bin/alfresco-repo-rebuild-amp
/usr/bin/alfresco-share-rebuild-amp

# Installing WAR files
ln -sf /usr/share/alfresco/bin/alfresco.war /usr/share/tomcat7/webapps
ln -sf /usr/share/alfresco/bin/share.war /usr/share/tomcat7/webapps

# Creating tomcat7 alfresco directory
ln -sf /usr/share/alfresco/extensions /usr/share/tomcat7/shared/classes/alfresco
ln -sf /usr/share/tomcat7/shared/classes/alfresco/extension/alfresco-global.properties /usr/share/tomcat7/shared/classes

# Fixing the MySQL library path for tomcat7
ln -sf /usr/share/java/mysql-jdbc.jar /usr/share/tomcat7/common/lib 

/sbin/chkconfig --add httpd
/sbin/chkconfig --add tomcat7

true

%preun
# If we have been uninstalled, remove our init scripts
# We shouldn't stop tomcat since we do not own it
if [ "$1" = 0 ]; then 
  /sbin/chkconfig --del alfresco
#  /sbin/chkconfig --del alfresco-ooo
fi

if [ $1 -eq 0 ] ; then 
  rm -f /usr/share/tomcat7/webapps/alfresco.war /usr/share/tomcat5/webapps/share.war
  rm -f /usr/share/tomcat7/shared/classes/alfresco
  rm -f /usr/share/alfresco/bin/alfresco.war
  rm -f /usr/share/alfresco/bin/share.war
fi
# Tomcat isn't good at keeping its cache up to date
rm -rf /usr/share/tomcat6/webapps/alfresco /usr/share/tomcat6/webapps/share

true

%postun
%{_initrddir}/tomcat5 condrestart


%files
%defattr(-,root,root,-)
# %{_initrddir}/alfresco-ooo
# %{_initrddir}/alfresco
/usr/bin/alfresco-repo-rebuild-amp
/usr/bin/alfresco-share-rebuild-amp
/usr/share/alfresco/bin/alfresco-real.war
/usr/share/alfresco/bin/share-real.war
/usr/share/alfresco/bin/alfresco-mmt.jar
/usr/share/alfresco/endorsed/
/usr/share/alfresco/commands/
/usr/share/alfresco/extras/
/usr/share/alfresco/extensions/messages/
/usr/share/alfresco/extensions/web-extension/
/usr/share/alfresco/extensions/extension/bootstrap/
/usr/share/alfresco/extensions/extension/mt/
/usr/share/alfresco/extensions/extension/*sample*
/usr/share/alfresco/extensions/extension/audit/
/usr/share/alfresco/repo-amp.d
/usr/share/alfresco/share-amp.d
%attr(0700,tomcat,tomcat) /var/lib/alfresco
%config(noreplace) /usr/share/alfresco/extensions/extension/alfresco-global.properties
%config(noreplace) /etc/httpd/conf.d/alfresco.conf
%config(noreplace) /etc/tomcat5/jk-workers.properties
%doc /usr/share/doc/alfresco-community-%{version}



%changelog
* Fri May 16 2014  <xkahn@redhat.com> - 4.2.f-1
- Initial RPMization


