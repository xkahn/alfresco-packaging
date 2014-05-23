This is a work in progress and requires some more work to get the package into a useable state. It does not comply
with the debian packaging policy mainly because I am still learning how that all fits together. Use at your own
risk. 

Build the deb pakcage:
======================
1. Download share.war and alfresco.war for version 4.2.f from the community site and place in the alfresco-4.2.f directory.
2. Make usre you have the relevant support packages installed, like dh-make to build the deb package
3  Change directory to the alfresco-4.2.f directory and run "fakeroot debian/rules binary"
4. The deb package will be in the root directory where you checked out the project. Run dpkg -i alfresco_4.2.f_xxx.deb
