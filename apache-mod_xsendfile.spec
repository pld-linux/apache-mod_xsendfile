%define		mod_name	xsendfile
%define 	apxs		/usr/sbin/apxs
Summary:	Apache module: convert character encoding of request URLs
Name:		apache-mod_%{mod_name}
Version:	0.8
Release:	0.1
License:	Apache 2.0
Group:		Networking/Daemons
Source0:	http://celebnamer.celebworld.ws/stuff/mod_xsendfile/mod_xsendfile-%{version}.tar.gz
# Source0-md5:	aa885ed32cce545404f329fdf507e53b
URL:		http://celebnamer.celebworld.ws/stuff/mod_xsendfile/
BuildRequires:	%{apxs}
BuildRequires:	apache-devel >= 2.0
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	apache(modules-api) = %apache_modules_api
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR 2>/dev/null)
%define		_sysconfdir	%(%{apxs} -q SYSCONFDIR 2>/dev/null)
%define		_pkglogdir	%(%{apxs} -q PREFIX 2>/dev/null)/logs

%description
mod_xsendfile is a small Apache2 module that processes X-SENDFILE
headers registered by the original output handler. If it encounters
the presence of such header it will discard all output and send the
file specified by that header instead using Apache internals including
all optimizations like caching-headers and sendfile or mmap if
configured. It is useful for processing script-output of e.g. PHP,
Perl or any CGI.

%prep
%setup -qc

%build
%{apxs} -c mod_%{mod_name}.c -o mod_%{mod_name}.la

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pkglibdir},%{_sysconfdir}/httpd.conf}

install .libs/mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}
echo 'LoadModule %{mod_name}_module modules/mod_%{mod_name}.so' > \
    $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf/90_mod_%{mod_name}.conf

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
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf/*_mod_%{mod_name}.conf
%attr(755,root,root) %{_pkglibdir}/*.so
