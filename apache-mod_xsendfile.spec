%define		mod_name	xsendfile
%define 	apxs		/usr/sbin/apxs
Summary:	Apache module: processing X-SENDFILE headers
Summary(pl.UTF-8):	Moduł Apache'a przetwarzający nagłówki X-SENDFILE
Name:		apache-mod_%{mod_name}
Version:	0.12
Release:	2
License:	Apache v2.0
Group:		Networking/Daemons/HTTP
Source0:	http://tn123.org/mod_xsendfile/mod_xsendfile-%{version}.tar.bz2
# Source0-md5:	4b83b0e1a0c043c4e76ee99685c35110
URL:		https://tn123.org/mod_xsendfile/
BuildRequires:	%{apxs}
BuildRequires:	apache-devel >= 2.0
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	apache(modules-api) = %apache_modules_api
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR 2>/dev/null)
%define		_sysconfdir	%(%{apxs} -q SYSCONFDIR 2>/dev/null)/conf.d

%description
mod_xsendfile is a small Apache2 module that processes X-SENDFILE
headers registered by the original output handler. If it encounters
the presence of such header it will discard all output and send the
file specified by that header instead using Apache internals including
all optimizations like caching-headers and sendfile or mmap if
configured. It is useful for processing script-output of e.g. PHP,
Perl or any CGI.

%description -l pl.UTF-8
mod_xsendfile to mały moduł Apache'a 2 przetwarzający nagłówki
X-SENDFILE zarejestrowane przez oryginalną procedurę obsługi wyjścia.
Kiedy stwierdzi obecność takiego nagłówka, anuluje całe wyjście i
zamiast niego wysyła plik wskazany przez ten nagłówek przy użyciu
funkcji wewnętrznych Apache'a wraz ze wszystkimi optymalizacjami,
takimi jak buforowanie nagłówków i sendfile/mmap. Moduł ten jest
przydatny do przetwarzania wyjścia skryptów, np. PHP, Perla czy
dowolnego CGI.

%prep
%setup -q -n mod_xsendfile-%{version}

%build
%{apxs} -c mod_%{mod_name}.c -o mod_%{mod_name}.la

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pkglibdir},%{_sysconfdir}}
install -p .libs/mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}
echo 'LoadModule %{mod_name}_module modules/mod_%{mod_name}.so' > \
    $RPM_BUILD_ROOT%{_sysconfdir}/90_mod_%{mod_name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%service -q httpd restart

%postun
if [ "$1" = "0" ]; then
	%service -q httpd restart
fi

%files
%defattr(644,root,root,755)
%doc docs/Readme.html
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*_mod_%{mod_name}.conf
%attr(755,root,root) %{_pkglibdir}/*.so
