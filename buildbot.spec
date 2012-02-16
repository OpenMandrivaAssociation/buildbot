%global slaveversion 0.8.5

Name:           buildbot
Version:        0.8.5
Release:        %mkrel 1
Summary:        Build/test automation system
Group:          Development/Python
License:        GPLv2+
URL:            http://buildbot.net
Source0:        http://buildbot.googlecode.com/files/%{name}-%{version}.tar.gz
Source1:        http://buildbot.googlecode.com/files/%{name}-slave-%{slaveversion}.tar.gz  
Patch0:         buildbot-contrib-shebang.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:  python-devel
BuildRequires:  python-sphinx
BuildRequires:  python-setuptools
Requires:       python-twisted >= 2.0.0
Requires:       python-jinja2
BuildArch:  noarch

# Turns former package into a metapackage for installing everything
Requires:       %{name}-master = %{version}
Requires:       %{name}-doc = %{version}
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

