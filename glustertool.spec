%define name glustertool
%define version 0.1.1
%define release 1

Summary: Gluster Tools
Name: %{name}
Version: %{version}
Release: %{release}
Source0: %{name}-%{version}.tar.gz
License: GPLv2
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix: %{_prefix}
BuildArch: noarch
Vendor: Aravinda VK <avishwan@redhat.com>
Url: https://github.com/gluster/glustertool

%description
Gluster Tools

%prep
%setup -n %{name}-%{version} -n %{name}-%{version}

%build
python setup.py build

%install
python setup.py install --single-version-externally-managed -O1 --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES

%clean
rm -rf $RPM_BUILD_ROOT

%files -f INSTALLED_FILES
%defattr(-,root,root)

%post

%preun

%changelog
* Mon Feb 15 2016 <avishwan@redhat.com>
- Initial Build
