Name:           buildbot
Version:        0.7.10p1
Release:        %mkrel 1
Summary:        Build/test automation system

Group:          Development/Python
License:        GPLv2+
URL:            http://buildbot.net
Source0:        http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot

BuildRequires:  python-devel
Requires:       python-twisted >= 2.0.0

%description
The BuildBot is a system to automate the compile/test cycle required by
most software projects to validate code changes. By automatically
rebuilding and testing the tree each time something has changed, build
problems are pinpointed quickly, before other developers are
inconvenienced by the failure.

%prep
%setup -q

%build
%{__python} setup.py build

%install
rm -rf %{buildroot}

%{__python} setup.py install -O1 --skip-build --root %{buildroot} --install-purelib=%py_platsitedir

mkdir -p %{buildroot}/%{_datadir}/%{name}/
cp -R contrib %{buildroot}/%{_datadir}/%{name}/

# clean up Windows contribs.
sed -i 's/\r//' %{buildroot}/%{_datadir}/%{name}/contrib/windows/*
chmod -x %{buildroot}/%{_datadir}/%{name}/contrib/windows/*

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc NEWS README docs
%{_bindir}/buildbot
%{py_platsitedir}/buildbot
%{_datadir}/%{name}
%{py_platsitedir}/*.egg-info
