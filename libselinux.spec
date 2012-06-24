Summary:	SELinux library and simple utilities
Summary(pl):	Biblioteka SELinux i proste narz�dzia
Name:		libselinux
Version:	1.16
Release:	1
Epoch:		0
License:	Public domain (uncopyrighted)
Group:		Libraries
Source0:	http://www.nsa.gov/selinux/archives/%{name}-%{version}.tgz
# Source0-md5:	0dfa39b41834904e58db14ddb881abb9
Patch0:		%{name}-rhat.patch
URL:		http://www.nsa.gov/selinux/
BuildRequires:	glibc-devel >= 6:2.3
Obsoletes:	selinux-libs
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_bindir		/bin

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

%description -l pl
Security-enhanced Linux jest prototypem j�dra Linuksa i wielu
aplikacji u�ytkowych o funkcjach podwy�szonego bezpiecze�stwa.
Zaprojektowany jest tak, aby w prosty spos�b ukaza� znaczenie
obowi�zkowej kontroli dost�pu dla spo�eczno�ci Linuksowej. Ukazuje
r�wnie� jak tak� kontrol� mo�na doda� do istniej�cego systemu typu
Linux. J�dro SELinux zawiera nowe sk�adniki architektury pierwotnie
opracowane w celu ulepszenia bezpiecze�stwa systemu operacyjnego
Flask. Te elementy zapewniaj� og�lne wsparcie we wdra�aniu wielu typ�w
polityk obowi�zkowej kontroli dost�pu, w��czaj�c te wzorowane na: Type
Enforcement (TE), kontroli dost�pu opartej na rolach (RBAC) i
zabezpieczeniach wielopoziomowych.

libselinux dostarcza API dla aplikacji SELinux aby mog�y pobiera� i
ustawia� procesy i konteksty plik�w w celu korzystania z polityki
bezpiecze�stwa. Bibilioteka jest wymagana przez wszystkie aplikacje,
kt�re u�ywaj� API SELinux.

%package devel
Summary:	Header files and devel documentation
Summary(pl):	Pliki nag��wkowe i dokumentacja programistyczna
Group:		Development/Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}
Obsoletes:	selinux-libs-devel

%description devel
Header files and devel documentation for SELinux libraries.

%description devel -l pl
Pliki nag��wkowe i dokumentacja programistyczna bibliotek SELinux.

%package static
Summary:	Static SELinux library
Summary(pl):	Biblioteki statyczne SELinux
Group:		Development/Libraries
Requires:	%{name}-devel = %{epoch}:%{version}-%{release}
Obsoletes:	selinux-static

%description static
SELinux static libraries.

%description static -l pl
Biblioteki statyczne SELinux.

%package utils
Summary:	SELinux utils
Summary(pl):	Narz�dzia SELinux
Group:		Applications/System
Requires:	%{name} = %{epoch}:%{version}-%{release}
Obsoletes:	selinux-utils

%description utils
SELinux utils.

%description utils -l pl
Narz�dzia SELinux.

%prep
%setup -q
%patch0 -p1

%build
%{__make} \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir},%{_includedir},/%{_lib}}

%{__make} install \
	LIBDIR="$RPM_BUILD_ROOT%{_libdir}" \
	SHLIBDIR="$RPM_BUILD_ROOT/%{_lib}" \
	DESTDIR="$RPM_BUILD_ROOT"

# make symlink across / absolute
ln -sf /%{_lib}/$(cd $RPM_BUILD_ROOT/%{_lib} ; echo libselinux.so.*) \
	$RPM_BUILD_ROOT%{_libdir}/libselinux.so

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) /%{_lib}/libselinux.so.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libselinux.so
%{_includedir}/selinux
%{_mandir}/man3/*.3*

%files static
%defattr(644,root,root,755)
%{_libdir}/libselinux.a

%files utils
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man8/*.8*
