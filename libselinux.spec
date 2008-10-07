#
# Conditional build:
%bcond_without	python	# python binding
#
Summary:	SELinux library and simple utilities
Summary(pl.UTF-8):	Biblioteka SELinux i proste narzędzia
Name:		libselinux
Version:	2.0.65
Release:	2
Epoch:		0
License:	Public Domain
Group:		Libraries
Source0:	http://www.nsa.gov/selinux/archives/%{name}-%{version}.tgz
# Source0-md5:	47e0d67e843a5cfacd3a27c89efc65e3
Patch0:		%{name}-vcontext-selinux.patch
URL:		http://www.nsa.gov/selinux/
%ifarch ppc ppc64 sparc sparcv9 sparc64
BuildRequires:	gcc >= 5:3.4
%else
BuildRequires:	gcc >= 5:3.2
%endif
BuildRequires:	glibc-devel >= 6:2.3
BuildRequires:	libsepol-devel >= 2.0.0
%{?with_python:BuildRequires:	python-devel}
%{?with_python:BuildRequires:	rpm-pythonprov}
BuildRequires:	sed >= 4.0
%{?with_python:BuildRequires:	swig-python}
Requires:	glibc(tls)
Requires:	libsepol >= 2.0.0
Obsoletes:	selinux-libs
Conflicts:	SysVinit < 2.86-4
ExcludeArch:	i386
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Security-enhanced Linux is a patch of the Linux kernel and a number
of utilities with enhanced security functionality designed to add
mandatory access controls to Linux. The Security-enhanced Linux kernel
contains new architectural components originally developed to improve
the security of the Flask operating system. These architectural
components provide general support for the enforcement of many kinds
of mandatory access control policies, including those based on the
concepts of Type Enforcement, Role-based Access Control, and
Multi-level Security.

libselinux provides an API for SELinux applications to get and set
process and file security contexts and to obtain security policy
decisions. Required for any applications that use the SELinux API.

%description -l pl.UTF-8
Security-enhanced Linux jest prototypem jądra Linuksa i wielu
aplikacji użytkowych o funkcjach podwyższonego bezpieczeństwa.
Zaprojektowany jest tak, aby w prosty sposób ukazać znaczenie
obowiązkowej kontroli dostępu dla społeczności linuksowej. Ukazuje
również jak taką kontrolę można dodać do istniejącego systemu typu
Linux. Jądro SELinux zawiera nowe składniki architektury pierwotnie
opracowane w celu ulepszenia bezpieczeństwa systemu operacyjnego
Flask. Te elementy zapewniają ogólne wsparcie we wdrażaniu wielu 
typów polityk obowiązkowej kontroli dostępu, włączając te wzorowane 
na: Type Enforcement (TE), kontroli dostępu opartej na rolach (RBAC) 
i zabezpieczeniach wielopoziomowych.

libselinux dostarcza API dla aplikacji SELinux aby mogły pobierać 
i ustawiać procesy i konteksty plików w celu korzystania z polityki
bezpieczeństwa. Biblioteka jest wymagana przez wszystkie aplikacje,
które używają API SELinux.

%package devel
Summary:	Header files and devel documentation
Summary(pl.UTF-8):	Pliki nagłówkowe i dokumentacja programistyczna
Group:		Development/Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}
Obsoletes:	selinux-libs-devel

%description devel
Header files and devel documentation for SELinux libraries.

%description devel -l pl.UTF-8
Pliki nagłówkowe i dokumentacja programistyczna bibliotek SELinux.

%package static
Summary:	Static SELinux library
Summary(pl.UTF-8):	Biblioteki statyczne SELinux
Group:		Development/Libraries
Requires:	%{name}-devel = %{epoch}:%{version}-%{release}
Obsoletes:	selinux-static

%description static
SELinux static libraries.

%description static -l pl.UTF-8
Biblioteki statyczne SELinux.

%package utils
Summary:	SELinux utils
Summary(pl.UTF-8):	Narzędzia SELinux
Group:		Applications/System
Requires:	%{name} = %{epoch}:%{version}-%{release}
Obsoletes:	selinux-utils

%description utils
SELinux utils.

%description utils -l pl.UTF-8
Narzędzia SELinux.

%package -n python-selinux
Summary:	Python binding for SELinux library
Summary(pl.UTF-8):	Wiązania Pythona do biblioteki SELinux
Group:		Libraries/Python
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description -n python-selinux
Python binding for SELinux library.

%description -n python-selinux -l pl.UTF-8
Wiązania Pythona do biblioteki SELinux.

%prep
%setup -q
%patch0 -p1

# "-z defs" doesn't mix with --as-needed when some object needs symbols from
# ld.so (because of __thread variable in this case)
sed -i -e 's/-z,defs,//' src/Makefile

%build
%{__make} all %{?with_python:pywrap} \
	CC="%{__cc}" \
	LDFLAGS="%{rpmldflags}" \
	CFLAGS="%{rpmcflags} -D_FILE_OFFSET_BITS=64" \
	LIBDIR=%{_libdir}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install %{?with_python:install-pywrap} \
	LIBDIR="$RPM_BUILD_ROOT%{_libdir}" \
	SHLIBDIR="$RPM_BUILD_ROOT/%{_lib}" \
	DESTDIR="$RPM_BUILD_ROOT"

# make symlink across / absolute
ln -sf /%{_lib}/$(basename $RPM_BUILD_ROOT/%{_lib}/libselinux.so.*) \
	$RPM_BUILD_ROOT%{_libdir}/libselinux.so

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc ChangeLog LICENSE
%attr(755,root,root) /%{_lib}/libselinux.so.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libselinux.so
%{_includedir}/selinux
%{_mandir}/man3/*.3*
%{_mandir}/man5/selabel_*.5*

%files static
%defattr(644,root,root,755)
%{_libdir}/libselinux.a

%files utils
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/*
%{_mandir}/man8/*.8*

%if %{with python}
%files -n python-selinux
%defattr(644,root,root,755)
%dir %{py_sitedir}/selinux
%attr(755,root,root) %{py_sitedir}/selinux/_selinux.so
%attr(755,root,root) %{py_sitedir}/selinux/audit2why.so
%{py_sitedir}/selinux/__init__.py
%endif
