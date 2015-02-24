#
# Conditional build:
%bcond_without	python	# Python binding
%bcond_without	ruby	# Ruby binding

%define	sepol_ver	2.3
Summary:	SELinux library and simple utilities
Summary(pl.UTF-8):	Biblioteka SELinux i proste narzędzia
Name:		libselinux
Version:	2.3
Release:	4
License:	Public Domain
Group:		Libraries
# git clone http://oss.tresys.com/git/selinux.git/
Source0:	http://userspace.selinuxproject.org/releases/current/%{name}-%{version}.tar.gz
# Source0-md5:	b11d4d95ef4bde732dbc8462df57a1e5
Patch0:		%{name}-vcontext-selinux.patch
URL:		https://github.com/SELinuxProject/selinux/wiki
%ifarch ppc ppc64 sparc sparcv9 sparc64
BuildRequires:	gcc >= 5:3.4
%else
BuildRequires:	gcc >= 5:3.2
%endif
BuildRequires:	glibc-devel >= 6:2.3
BuildRequires:	libsepol-devel >= %{sepol_ver}
%{?with_python:BuildRequires:	libsepol-static >= %{sepol_ver}}
BuildRequires:	pcre-devel
BuildRequires:	pkgconfig
%{?with_python:BuildRequires:	python-devel}
%{?with_python:BuildRequires:	rpm-pythonprov}
BuildRequires:	rpmbuild(macros) >= 1.696
%{?with_ruby:BuildRequires:	ruby-devel >= 1.9}
BuildRequires:	sed >= 4.0
%{?with_python:BuildRequires:	swig-python}
%{?with_ruby:BuildRequires:	swig-ruby}
Requires:	glibc(tls)
Requires:	libsepol >= %{sepol_ver}
Obsoletes:	selinux-libs
Conflicts:	SysVinit < 2.86-4
ExcludeArch:	i386
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Security-enhanced Linux is a patch of the Linux kernel and a number of
utilities with enhanced security functionality designed to add
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
Flask. Te elementy zapewniają ogólne wsparcie we wdrażaniu wielu typów
polityk obowiązkowej kontroli dostępu, włączając te wzorowane na: Type
Enforcement (TE), kontroli dostępu opartej na rolach (RBAC) i
zabezpieczeniach wielopoziomowych.

libselinux dostarcza API dla aplikacji SELinux aby mogły pobierać i
ustawiać procesy i konteksty plików w celu korzystania z polityki
bezpieczeństwa. Biblioteka jest wymagana przez wszystkie aplikacje,
które używają API SELinux.

%package devel
Summary:	Header files and devel documentation
Summary(pl.UTF-8):	Pliki nagłówkowe i dokumentacja programistyczna
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libsepol-devel >= %{sepol_ver}
Obsoletes:	selinux-libs-devel

%description devel
Header files and devel documentation for SELinux libraries.

%description devel -l pl.UTF-8
Pliki nagłówkowe i dokumentacja programistyczna bibliotek SELinux.

%package static
Summary:	Static SELinux library
Summary(pl.UTF-8):	Biblioteki statyczne SELinux
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Obsoletes:	selinux-static

%description static
SELinux static libraries.

%description static -l pl.UTF-8
Biblioteki statyczne SELinux.

%package utils
Summary:	SELinux utils
Summary(pl.UTF-8):	Narzędzia SELinux
Group:		Applications/System
Requires:	%{name} = %{version}-%{release}
Obsoletes:	selinux-utils

%description utils
SELinux utils.

%description utils -l pl.UTF-8
Narzędzia SELinux.

%package -n python-selinux
Summary:	Python binding for SELinux library
Summary(pl.UTF-8):	Wiązania Pythona do biblioteki SELinux
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}

%description -n python-selinux
Python binding for SELinux library.

%description -n python-selinux -l pl.UTF-8
Wiązania Pythona do biblioteki SELinux.

%package -n ruby-selinux
Summary:	Ruby binding for SELinux library
Summary(pl.UTF-8):	Wiązania języka Ruby do biblioteki SELinux
Group:		Development/Languages
Requires:	%{name} = %{version}-%{release}

%description -n ruby-selinux
Ruby binding for SELinux library.

%description -n ruby-selinux -l pl.UTF-8
Wiązania języka Ruby do biblioteki SELinux.

%prep
%setup -q
%patch0 -p1

# "-z defs" doesn't mix with --as-needed when some object needs symbols from
# ld.so (because of __thread variable in this case)
sed -i -e 's/-z,defs,//' src/Makefile

%build
%{__make} -j1 all %{?with_python:pywrap} %{?with_ruby:rubywrap} \
	CC="%{__cc}" \
	CFLAGS="%{rpmcppflags} %{rpmcflags} -D_FILE_OFFSET_BITS=64" \
	LDFLAGS="%{rpmldflags} -lpcre -lpthread" \
	LIBDIR=%{_libdir} \
	%{?with_ruby:RUBYINC="$(pkg-config --cflags ruby-%{ruby_abi})"}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install %{?with_python:install-pywrap} %{?with_ruby:install-rubywrap} \
	LIBDIR=$RPM_BUILD_ROOT%{_libdir} \
	SHLIBDIR=$RPM_BUILD_ROOT/%{_lib} \
	RUBYINSTALL=$RPM_BUILD_ROOT%{ruby_vendorarchdir} \
	DESTDIR=$RPM_BUILD_ROOT \

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
%{_mandir}/man5/booleans.5*
%{_mandir}/man5/customizable_types.5*
%{_mandir}/man5/default_contexts.5*
%{_mandir}/man5/default_type.5*
%{_mandir}/man5/failsafe_context.5*
%{_mandir}/man5/file_contexts.homedirs.5*
%{_mandir}/man5/file_contexts.local.5
%{_mandir}/man5/file_contexts.subs.5
%{_mandir}/man5/file_contexts.subs_dist.5
%{_mandir}/man5/local.users.5*
%{_mandir}/man5/removable_context.5*
%{_mandir}/man5/secolor.conf.5*
%{_mandir}/man5/securetty_types.5*
%{_mandir}/man5/service_seusers.5*
%{_mandir}/man5/seusers.5*
%{_mandir}/man5/user_contexts.5*
%{_mandir}/man5/virtual_domain_context.5*
%{_mandir}/man5/virtual_image_context.5*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libselinux.so
%{_pkgconfigdir}/libselinux.pc
%{_includedir}/selinux
%{_mandir}/man3/*.3*
%{_mandir}/man5/file_contexts.5*
%{_mandir}/man5/media.5*
%{_mandir}/man5/selabel_*.5*
%{_mandir}/man5/sepgsql_contexts.5*
%{_mandir}/man5/x_contexts.5*

%files static
%defattr(644,root,root,755)
%{_libdir}/libselinux.a

%files utils
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/avcstat
%attr(755,root,root) %{_sbindir}/compute_*
%attr(755,root,root) %{_sbindir}/getconlist
%attr(755,root,root) %{_sbindir}/getdefaultcon
%attr(755,root,root) %{_sbindir}/getenforce
%attr(755,root,root) %{_sbindir}/getfilecon
%attr(755,root,root) %{_sbindir}/getpidcon
%attr(755,root,root) %{_sbindir}/getsebool
%attr(755,root,root) %{_sbindir}/getseuser
%attr(755,root,root) %{_sbindir}/matchpathcon
%attr(755,root,root) %{_sbindir}/policyvers
%attr(755,root,root) %{_sbindir}/selinux*
%attr(755,root,root) %{_sbindir}/setenforce
%attr(755,root,root) %{_sbindir}/sefcontext_compile
%attr(755,root,root) %{_sbindir}/setfilecon
%attr(755,root,root) %{_sbindir}/togglesebool
%{_mandir}/man8/avcstat.8*
%{_mandir}/man8/booleans.8*
%{_mandir}/man8/getenforce.8*
%{_mandir}/man8/getsebool.8*
%{_mandir}/man8/matchpathcon.8*
%{_mandir}/man8/sefcontext_compile.8*
%{_mandir}/man8/selinux*.8*
%{_mandir}/man8/setenforce.8*
%{_mandir}/man8/togglesebool.8*

%if %{with python}
%files -n python-selinux
%defattr(644,root,root,755)
%dir %{py_sitedir}/selinux
%attr(755,root,root) %{py_sitedir}/selinux/_selinux.so
%attr(755,root,root) %{py_sitedir}/selinux/audit2why.so
%{py_sitedir}/selinux/__init__.py
%endif

%if %{with ruby}
%files -n ruby-selinux
%defattr(644,root,root,755)
%attr(755,root,root) %{ruby_vendorarchdir}/selinux.so
%endif
