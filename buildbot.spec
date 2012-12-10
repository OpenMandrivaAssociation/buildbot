%global slaveversion 0.8.5

Name:           buildbot
Version:        0.8.5
Release:        %mkrel 2
Summary:        Build/test automation system
Group:          Development/Python
License:        GPLv2+
URL:            http://buildbot.net
Source0:        http://buildbot.googlecode.com/files/%{name}-%{version}.tar.gz
Source1:        http://buildbot.googlecode.com/files/%{name}-slave-%{slaveversion}.tar.gz  
Patch0:         buildbot-contrib-shebang.patch
Patch1:         buildbot-alchemy-migrate-req.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:  python-devel
BuildRequires:  python-sphinx
BuildRequires:  python-setuptools
Requires:       python-twisted >= 2.0.0
Requires:       python-jinja2
BuildArch:  noarch

# Turns former package into a metapackage for installing everything
Requires:       %{name}-master = %{version}
#docs disabled
#%%Requires:       %{name}-doc = %{version}
Requires:       %{name}-slave = %{slaveversion}

%description
The BuildBot is a system to automate the compile/test cycle required by
most software projects to validate code changes. By automatically
rebuilding and testing the tree each time something has changed, build
problems are pinpointed quickly, before other developers are
inconvenienced by the failure.

%package master
Summary:        Build/test automation system
Group:          Development/Python
License:        GPLv2+

%description master
The BuildBot is a system to automate the compile/test cycle required by
most software projects to validate code changes. By automatically
rebuilding and testing the tree each time something has changed, build
problems are pinpointed quickly, before other developers are
inconvenienced by the failure.

%package slave
Version:        %{slaveversion}   
Summary:        Build/test automation system
Group:          Development/Python
License:        GPLv2

%description slave
This package contains only the buildslave implementation.
The buildbot-master package contains the buildmaster.


#%%package doc
#Summary:    Buildbot documentation
#Group:      Documentation

#%%description doc
#Buildbot documentation

%prep
%setup -q -b 1 -n %{name}-slave-%{slaveversion}
%setup -q
%patch0 -p0
%patch1 -p0

# include only generated images in binary rpm
#mkdir images && mv docs/images/*.png images/

%build
%{__python} setup.py build

# disable for now, tarball is borked
#pushd docs
#make docs.tgz
#popd

pushd ../%{name}-slave-%{slaveversion}
%{__python} setup.py build
popd

%install
rm -rf %{buildroot}

%{__python} setup.py install -O1 --skip-build --root %{buildroot}

mkdir -p %{buildroot}%{_datadir}/%{name}/ \
         %{buildroot}%{_mandir}/man1/ \
#         %{buildroot}%{_docdir}/%{name}-%{version}

cp -R contrib %{buildroot}/%{_datadir}/%{name}/

# install the man page
cp docs/buildbot.1 %{buildroot}%{_mandir}/man1/buildbot.1

# install HTML documentation
#tar xf docs/docs.tgz --strip-components=1 -C %{buildroot}%{_docdir}/%{name}-%{version}

# clean up Windows contribs.
sed -i 's/\r//' %{buildroot}/%{_datadir}/%{name}/contrib/windows/*
chmod -x %{buildroot}/%{_datadir}/%{name}/contrib/windows/*

# install slave files
cd ../%{name}-slave-%{slaveversion}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

# Fix permissions
chmod 0755 %{buildroot}/%{_datadir}/%{name}/contrib/fix_changes_pickle_encoding.py

%clean
rm -rf %{buildroot}

%files

%files master
%defattr(-,root,root,-)
%doc COPYING CREDITS NEWS README UPGRADING
%doc %{_mandir}/man1/buildbot.1.xz
%{_bindir}/buildbot
%{python_sitelib}/buildbot
%{python_sitelib}/buildbot-*.egg-info
%{_datadir}/%{name}

%files slave
%doc COPYING NEWS README UPGRADING
%defattr(-,root,root,-)
%{_bindir}/buildslave
%{python_sitelib}/buildslave
%{python_sitelib}/buildbot_slave*.egg-info



%changelog
* Tue Feb 28 2012 Guilherme Moro <guilherme@mandriva.com> 0.8.5-2mdv2012.0
+ Revision: 781292
- Fixed reqs for buildbot-master

* Thu Feb 16 2012 Guilherme Moro <guilherme@mandriva.com> 0.8.5-1
+ Revision: 775248
+ rebuild (emptylog)

* Mon Feb 06 2012 Guilherme Moro <guilherme@mandriva.com> 0.8.5-0
+ Revision: 771323
- updated to version 0.8.5

* Sat Nov 06 2010 Jani Välimaa <wally@mandriva.org> 0.8.0-3mdv2011.0
+ Revision: 594296
- rebuild for python 2.7

  + Michael Scherer <misc@mandriva.org>
    - rebuild for python 2.7

  + Tadej Panjtar <tadej@mandriva.org>
    - update to 0.8.0

* Wed May 05 2010 Funda Wang <fwang@mandriva.org> 0.7.12-2mdv2010.1
+ Revision: 542308
- BR python-setuptools

* Sat Mar 06 2010 Sandro Cazzaniga <kharec@mandriva.org> 0.7.12-1mdv2010.1
+ Revision: 515258
- update to 0.7.12

* Mon Dec 14 2009 Stéphane Téletchéa <steletch@mandriva.org> 0.7.11p3-3mdv2010.1
+ Revision: 478465
- rpm-mandriva-setup fixed

* Mon Dec 14 2009 Stéphane Téletchéa <steletch@mandriva.org> 0.7.11p3-2mdv2010.1
+ Revision: 478462
- Provide a more clear explanation for the debugfiles list bug in rpm-mandriva-setup

* Fri Dec 11 2009 Stéphane Téletchéa <steletch@mandriva.org> 0.7.11p3-1mdv2010.1
+ Revision: 476461
- fix permissions for emit.py
- Fix error on debug search in the bs

  + Tadej Panjtar <tadej@mandriva.org>
    - minor corrections according to packaging standards
    - Update to new version

* Thu Sep 10 2009 Thierry Vignaud <tv@mandriva.org> 0.7.10p1-2mdv2010.0
+ Revision: 436903
- rebuild

* Thu Mar 05 2009 Jérôme Soyer <saispo@mandriva.org> 0.7.10p1-1mdv2009.1
+ Revision: 348914
- New upstream release

* Sun Dec 28 2008 Funda Wang <fwang@mandriva.org> 0.7.9-1mdv2009.1
+ Revision: 320366
- New version 0.7.9

* Mon Aug 11 2008 Jérôme Soyer <saispo@mandriva.org> 0.7.8-1mdv2009.0
+ Revision: 270612
- New release 0.7.8

* Thu Aug 07 2008 Thierry Vignaud <tv@mandriva.org> 0.7.7-2mdv2009.0
+ Revision: 266429
- rebuild early 2009.0 package (before pixel changes)

* Thu Apr 17 2008 Funda Wang <fwang@mandriva.org> 0.7.7-1mdv2009.0
+ Revision: 195060
- New version 0.7.7

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Tue Oct 09 2007 Jérôme Soyer <saispo@mandriva.org> 0.7.6-1mdv2008.1
+ Revision: 95946
- New release 0.7.6
- New release 0.7.6

* Thu Sep 27 2007 Anne Nicolas <ennael@mandriva.org> 0.7.5-3mdv2008.0
+ Revision: 93423
- bump release to reupload

* Wed Jun 06 2007 Jérôme Soyer <saispo@mandriva.org> 0.7.5-2mdv2008.0
+ Revision: 36098
- Fix %%mkrel number
- Bump release for rebuild
- Remove noarch
- Fix 64bits Build
- Fix RPM Group
- Import buildbot

