Summary:	A powerful pattern matching system for parsing and processing text
Summary(pl.UTF-8):	Potężny system dopasowywania wzorców do analizy i przetwarzania tekstu
Name:		grok
%define	snap	20170721
%define	gitref	a52f42b1fa359db2145a70216ec5b4ef43d57b5c
# git history shows 1.2011xxxx, then 0.9.y... use 0 for now
Version:	0
Release:	0.%{snap}.1
License:	BSD
Group:		Libaries
#Source0Download: https://github.com/jordansissel/grok/releases
Source0:	https://github.com/jordansissel/grok/archive/%{gitref}/%{name}-%{snap}.tar.gz
# Source0-md5:	1d09b3aa6ebac202680227faa26e742e
Patch0:		%{name}-gperf.patch
Patch1:		%{name}-bison.patch
URL:		https://github.com/jordansissel/grok
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	gperf
BuildRequires:	libevent-devel
BuildRequires:	pcre-devel >= 7.6
BuildRequires:	tokyocabinet-devel >= 1.4.9
Requires:	pcre >= 7.6
Requires:	tokyocabinet-libs >= 1.4.9
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A powerful pattern matching system for parsing and processing text
data such as log files.

%description -l pl.UTF-8
Potężny system dopasowywania wzorców do analizy i przetwarzania danych
tekstowych, takich jak pliki logów.

%package devel
Summary:	Grok development headers
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki grok
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	pcre-devel >= 7.6
Requires:	tokyocabinet-devel >= 1.4.9

%description devel
Headers required for grok development.

%description devel -l pl.UTF-8
Pliki nagłówkowe do tworzenia programów z użyciem biblioteki grok.

%prep
%setup -q -n %{name}-%{gitref}
%patch0 -p1
%patch1 -p1

%build
%{__make} \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags} -fPIC -pipe -I. -DPLATFORM_GNULinux" \
	LDFLAGS="%{rpmldflags} -rdynamic -lpcre -levent -ltokyocabinet -ldl"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir},%{_includedir},%{_datadir}/grok/patterns}

install grok discogrok $RPM_BUILD_ROOT%{_bindir}
install libgrok.so $RPM_BUILD_ROOT%{_libdir}/libgrok.so.1.0
ln -sf libgrok.so.1.0 $RPM_BUILD_ROOT%{_libdir}/libgrok.so.1
ln -sf libgrok.so.1.0 $RPM_BUILD_ROOT%{_libdir}/libgrok.so
cp -p patterns/base $RPM_BUILD_ROOT%{_datadir}/grok/patterns/base
cp -p grok.h grok_pattern.h grok_capture.h grok_capture_xdr.h grok_match.h grok_logging.h grok_discover.h grok_version.h \
	$RPM_BUILD_ROOT%{_includedir}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/discogrok
%attr(755,root,root) %{_bindir}/grok
%attr(755,root,root) %{_libdir}/libgrok.so.1.0
%attr(755,root,root) %ghost %{_libdir}/libgrok.so.1
%{_datadir}/grok

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgrok.so
%{_includedir}/grok*.h
