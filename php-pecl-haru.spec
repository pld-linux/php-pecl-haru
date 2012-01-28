%define		_modname	haru
%define		_status		stable
Summary:	%{_modname} - Haru PDF functions
Summary(pl.UTF-8):	%{_modname} - funkcje PDF haru
Name:		php-pecl-%{_modname}
Version:	1.0.0
Release:	4
License:	PHP
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{_modname}-%{version}.tgz
# Source0-md5:	967b9cf8394432547ce850ef6a3fb375
Patch0:		%{name}-pathfix.patch
URL:		http://pecl.php.net/package/haru/
BuildRequires:	libharu-devel >= 2.0.8-2
BuildRequires:	php-devel >= 3:5.0.0
BuildRequires:	rpmbuild(macros) >= 1.344
%{?requires_php_extension}
Requires:	php-common >= 4:5.0.4
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This extensions allows you to create PDF documents using the Haru Free
PDF Library.

In PECL status of this extension is: %{_status}.

%description -l pl.UTF-8
Rozszerzenie to pozwala na tworzenie dokumentów PDF przy użyciu
biblioteki Haru.

To rozszerzenie ma w PECL status: %{_status}.

%prep
%setup -q -c
mv %{_modname}-%{version}/* .
%patch0 -p1

%build
phpize
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d

%{__make} install \
	INSTALL_ROOT=$RPM_BUILD_ROOT \
	EXTENSION_DIR=%{php_extensiondir}
cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{_modname}.ini
; Enable %{_modname} extension module
extension=%{_modname}.so
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
%php_webserver_restart

%postun
if [ "$1" = 0 ]; then
	%php_webserver_restart
fi

%files
%defattr(644,root,root,755)
%doc CREDITS
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{_modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{_modname}.so
