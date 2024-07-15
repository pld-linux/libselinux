#
# Conditional build:
%bcond_without	python	# Python 3 binding
%bcond_without	ruby	# Ruby binding

%define	sepol_ver	3.7
Summary:	SELinux library and simple utilities
Summary(pl.UTF-8):	Biblioteka SELinux i proste narzędzia
Name:		libselinux
Version:	3.7
Release:	1
License:	Public Domain
Group:		Libraries
#Source0Download: https://github.com/SELinuxProject/selinux/wiki/Releases
Source0:	https://github.com/SELinuxProject/selinux/releases/download/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	ac0c812124d83faa7721928d0c01adc0
URL:		https://github.com/SELinuxProject/selinux/wiki
%ifarch ppc ppc64 sparc sparcv9 sparc64
BuildRequires:	gcc >= 5:3.4
%else
BuildRequires:	gcc >= 5:3.2
%endif
BuildRequires:	glibc-devel >= 6:2.3
BuildRequires:	libsepol-devel >= %{sepol_ver}
%{?with_python:BuildRequires:	libsepol-static >= %{sepol_ver}}
BuildRequires:	pcre2-8-devel
BuildRequires:	pkgconfig
%{?with_python:BuildRequires:	python3-devel >= 1:3.2}
%{?with_python:BuildRequires:	python3-pip}
%{?with_python:BuildRequires:	rpm-pythonprov}
BuildRequires:	rpmbuild(macros) >= 1.714
%{?with_ruby:BuildRequires:	ruby-devel >= 1.9}
BuildRequires:	sed >= 4.0
%{?with_python:BuildRequires:	swig-python >= 2}
%{?with_ruby:BuildRequires:	swig-ruby}
Requires:	glibc(tls)
Requires:	libsepol >= %{sepol_ver}
Obsoletes:	selinux-libs < 20030601
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
Obsoletes:	selinux-libs-devel < 20030601

%description devel
Header files and devel documentation for SELinux libraries.

%description devel -l pl.UTF-8
Pliki nagłówkowe i dokumentacja programistyczna bibliotek SELinux.

%package static
Summary:	Static SELinux library
Summary(pl.UTF-8):	Biblioteki statyczne SELinux
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Obsoletes:	selinux-static < 20030601

%description static
SELinux static libraries.

%description static -l pl.UTF-8
Biblioteki statyczne SELinux.

%package utils
Summary:	SELinux utils
Summary(pl.UTF-8):	Narzędzia SELinux
Group:		Applications/System
Requires:	%{name} = %{version}-%{release}
Obsoletes:	selinux-utils < 20030601

%description utils
SELinux utils.

%description utils -l pl.UTF-8
Narzędzia SELinux.

%package -n python3-selinux
Summary:	Python 3 binding for SELinux library
Summary(pl.UTF-8):	Wiązania Pythona 3 do biblioteki SELinux
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}

%description -n python3-selinux
Python 3 binding for SELinux library.

%description -n python3-selinux -l pl.UTF-8
Wiązania Pythona 3 do biblioteki SELinux.

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

%build
%{__make} -j1 all %{?with_python:pywrap} %{?with_ruby:rubywrap} \
	CC="%{__cc}" \
	CFLAGS="%{rpmcppflags} %{rpmcflags} -D_FILE_OFFSET_BITS=64" \
	LDFLAGS="%{rpmldflags}" \
	LIBDIR=%{_libdir} \
	PYPREFIX=python3 \
	PYSITEDIR=%{py3_sitedir} \
	PYTHON=%{__python3} \
	%{?with_ruby:RUBYINC="$(pkg-config --cflags ruby-%{ruby_abi})"}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install %{?with_python:install-pywrap} %{?with_ruby:install-rubywrap} \
	LIBDIR=%{_libdir} \
	SHLIBDIR=/%{_lib} \
	PYPREFIX=python3 \
	PYSITEDIR=%{py3_sitedir} \
	PYTHON=%{__python3} \
	RUBYINSTALL=%{ruby_vendorarchdir} \
	DESTDIR=$RPM_BUILD_ROOT

# make symlink across / absolute
ln -sf /%{_lib}/$(basename $RPM_BUILD_ROOT/%{_lib}/libselinux.so.*) \
	$RPM_BUILD_ROOT%{_libdir}/libselinux.so

%if %{with python}
%py3_comp $RPM_BUILD_ROOT%{py3_sitedir}/selinux
%py3_ocomp $RPM_BUILD_ROOT%{py3_sitedir}/selinux
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc LICENSE
%attr(755,root,root) /%{_lib}/libselinux.so.*
%{_mandir}/man5/customizable_types.5*
%{_mandir}/man5/default_contexts.5*
%{_mandir}/man5/default_type.5*
%{_mandir}/man5/failsafe_context.5*
%{_mandir}/man5/file_contexts.homedirs.5*
%{_mandir}/man5/file_contexts.local.5
%{_mandir}/man5/file_contexts.subs.5
%{_mandir}/man5/file_contexts.subs_dist.5
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
%{_mandir}/man3/avc_*.3*
%{_mandir}/man3/checkPasswdAccess.3*
%{_mandir}/man3/context_*.3*
%{_mandir}/man3/fgetfilecon*.3*
%{_mandir}/man3/fini_selinuxmnt.3*
%{_mandir}/man3/freecon*.3*
%{_mandir}/man3/fsetfilecon*.3*
%{_mandir}/man3/get_default_context*.3*
%{_mandir}/man3/get_default_type.3*
%{_mandir}/man3/get_ordered_context_list*.3*
%{_mandir}/man3/getcon*.3*
%{_mandir}/man3/getexeccon*.3*
%{_mandir}/man3/getfilecon*.3*
%{_mandir}/man3/getfscreatecon*.3*
%{_mandir}/man3/getkeycreatecon*.3*
%{_mandir}/man3/getpeercon*.3*
%{_mandir}/man3/getpidcon*.3*
%{_mandir}/man3/getpidprevcon*.3*
%{_mandir}/man3/getprevcon*.3*
%{_mandir}/man3/getseuserbyname.3*
%{_mandir}/man3/getsockcreatecon*.3*
%{_mandir}/man3/init_selinuxmnt.3*
%{_mandir}/man3/is_context_customizable.3*
%{_mandir}/man3/is_selinux_*.3*
%{_mandir}/man3/lgetfilecon*.3*
%{_mandir}/man3/lsetfilecon*.3*
%{_mandir}/man3/manual_user_enter_context.3*
%{_mandir}/man3/matchmediacon.3*
%{_mandir}/man3/matchpathcon*.3*
%{_mandir}/man3/mode_to_security_class.3*
%{_mandir}/man3/print_access_vector.3*
%{_mandir}/man3/query_user_context.3*
%{_mandir}/man3/rpm_execcon.3*
%{_mandir}/man3/security_*.3*
%{_mandir}/man3/selabel_*.3*
%{_mandir}/man3/selinux_*.3*
%{_mandir}/man3/set_matchpathcon_*.3*
%{_mandir}/man3/set_selinuxmnt.3*
%{_mandir}/man3/setcon*.3*
%{_mandir}/man3/setexeccon*.3*
%{_mandir}/man3/setexecfilecon*.3*
%{_mandir}/man3/setfilecon*.3*
%{_mandir}/man3/setfscreatecon*.3*
%{_mandir}/man3/setkeycreatecon*.3*
%{_mandir}/man3/setsockcreatecon*.3*
%{_mandir}/man3/sidget.3*
%{_mandir}/man3/sidput.3*
%{_mandir}/man3/string_to_av_perm.3*
%{_mandir}/man3/string_to_security_class.3*
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
%attr(755,root,root) %{_sbindir}/getpidprevcon
%attr(755,root,root) %{_sbindir}/getpolicyload
%attr(755,root,root) %{_sbindir}/getsebool
%attr(755,root,root) %{_sbindir}/getseuser
%attr(755,root,root) %{_sbindir}/matchpathcon
%attr(755,root,root) %{_sbindir}/policyvers
%attr(755,root,root) %{_sbindir}/selabel_digest
%attr(755,root,root) %{_sbindir}/selabel_get_digests_all_partial_matches
%attr(755,root,root) %{_sbindir}/selabel_lookup
%attr(755,root,root) %{_sbindir}/selabel_lookup_best_match
%attr(755,root,root) %{_sbindir}/selabel_partial_match
%attr(755,root,root) %{_sbindir}/selinux*
%attr(755,root,root) %{_sbindir}/setenforce
%attr(755,root,root) %{_sbindir}/sefcontext_compile
%attr(755,root,root) %{_sbindir}/setfilecon
%attr(755,root,root) %{_sbindir}/togglesebool
%attr(755,root,root) %{_sbindir}/validatetrans
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
%files -n python3-selinux
%defattr(644,root,root,755)
%dir %{py3_sitedir}/selinux
%attr(755,root,root) %{py3_sitedir}/_selinux.cpython-*.so
%attr(755,root,root) %{py3_sitedir}/selinux/_selinux.cpython-*.so
%attr(755,root,root) %{py3_sitedir}/selinux/audit2why.cpython-*.so
%{py3_sitedir}/selinux/__init__.py
%{py3_sitedir}/selinux/__pycache__
%{py3_sitedir}/selinux-%{version}-py*.egg-info
%endif

%if %{with ruby}
%files -n ruby-selinux
%defattr(644,root,root,755)
%attr(755,root,root) %{ruby_vendorarchdir}/selinux.so
%endif
