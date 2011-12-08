%define WTSRVDIR /var/spool/wt
%define WTRUNDIR %{WTSRVDIR}/run

%define WTRUNUSER apache
%define WTRUNGROUP apache

Summary:    Web Toolkit
Name:       wt
Version:    3.2.0
Release:    1%{?dist}.R

Url:        http://www.webtoolkit.eu/wt
License:    GPLv2
Group:      Development/Libraries
Source0:    http://citylan.dl.sourceforge.net/project/witty/wt/%{version}/%{name}-%{version}.tar.gz

BuildRequires:  fcgi-devel
BuildRequires:  xerces-c-devel
BuildRequires:  openssl-devel
BuildRequires:  boost-devel >= 1.36
BuildRequires:  mxml-devel >= 2.3
BuildRequires:  postgresql-devel
BuildRequires:  postgresql-libs
BuildRequires:  cmake
BuildRequires:  doxygen
BuildRequires:  gd-devel
BuildRequires:  qt4-devel
BuildRequires:  pkgconfig
BuildRequires:  pango-devel
BuildRequires:  libharu-devel
BuildRequires:  GraphicsMagick-devel

%description
Wt is a C++ library and application server for developing and
deploying web applications. The widget-centric API is inspired by
existing C++ GUI APIs. It offers complete abstraction of any
web-specific implementation details.  Most importantly, the entire
application is written in only one compiled language (C++), from which
the library generates the necessary HTML, Javascript, CGI, and AJAX
code.


%package devel
Summary:    Web Toolkit
Group:      Development/Libraries
Requires:   %{name} = %{version}


%description devel
The %{name}-devel package contains libraries and header files for
developing extensions for %{name}.


%prep
%setup -q


%build
mkdir wt-build
cd wt-build
CFLAGS=$RPM_OPT_FLAGS CXXFLAGS="$RPM_OPT_FLAGS" \
%{cmake} .. \
    -DCONNECTOR_HTTP=ON \
    -DCONNECTOR_FCGI=ON \
    -DWEBGROUP="%{WTRUNGROUP}" -DWEBUSER="%{WTRUNUSER}" \
    -DRUNDIR="%{WTRUNDIR}"

make %{?_smp_mflags}

%install
rm -rf %{buildroot}
cd wt-build
make DESTDIR=%{buildroot} install

mkdir -p %{buildroot}/%{WTSRVDIR}
mkdir -p %{buildroot}/%{WTRUNDIR}
mv -v %{buildroot}/%{_datadir}/Wt %{buildroot}/%{_datadir}/wt

# We mustn't package .orig files
find %{buildroot}/%{_includedir}/Wt -name '*.orig' -delete


%clean
rm -rf %{buildroot}


%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig


%files
%defattr(-,root,root)
%doc README.md Changelog INSTALL LICENSE
%{_libdir}/*.so.*
%dir %{_sysconfdir}/%{name}
%{_datadir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/wt_config.xml
%attr(-,%{WTRUNUSER},%{WTRUNGROUP}) %{WTRUNDIR}


%files devel
%defattr(-,root,root)
%{_includedir}/Wt
%{_libdir}/*.so
%{_datadir}/cmake*/Modules/*


%changelog
* Thu Dec 08 2011 Vasiliy N. Glazov <vascom2@gmail.com> - 3.2.0-1.R
- update to 3.2.0

* Tue Sep 27 2011 Vasiliy N. Glazov <vascom2@gmail.com> - 3.1.11-1.R
- update to 3.1.11

* Wed Sep 21 2011 Vasiliy N. Glazov <vascom2@gmail.com> - 3.1.10-2.R
- Added more buildrequires and functionality

* Fri Jul 29 2011 Vasiliy N. Glazov <vascom2@gmail.com> - 3.1.10-1.R
- update to 3.1.10

* Sun Mar 20 2011 Arkady L. Shane <ashejn@yandex-team.ru> - 3.1.8-1
- update to 3.1.8

* Tue Nov 16 2010 Arkady L. Shane <ashejn@yandex-team.ru> - 3.1.6-1
- update to 3.1.6

* Fri Aug 20 2010 Arkady L. Shane <ashejn@yandex-team.ru> - 3.1.4-1
- update to 3.1.4

* Mon Aug  9 2010 Arkady L. Shane <ashejn@yandex-team.ru> - 3.1.3-1
- initial build for Fedora
