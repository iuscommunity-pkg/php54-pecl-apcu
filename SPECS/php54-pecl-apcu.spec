# spec file for php-pecl-apcu
#
# Copyright (c) 2013 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/3.0/
#
# Please, preserve the changelog entries
#
%if 0%{?scl:1}
%scl_package php-pecl-apcu
%else
%global pkg_name %{name}
%global _root_sysconfdir %{_sysconfdir}
%endif

%{!?php_inidir:  %{expand: %%global php_inidir  %{_sysconfdir}/php.d}}
%{!?php_incldir: %{expand: %%global php_incldir %{_includedir}/php}}
%{!?__pecl:      %{expand: %%global __pecl      %{_bindir}/pecl}}
%global pecl_name apcu
%global with_zts  0%{?__ztsphp:1}
%define php_base php54
%define real_name php-pecl-apcu

Name:           %{?scl_prefix}%{php_base}-pecl-apcu
Summary:        APC User Cache
Version:        4.0.1
Release:        4.ius%{?dist}
Source0:        http://pecl.php.net/get/%{pecl_name}-%{version}.tgz
Source1:        %{pecl_name}.ini
Source2:        %{pecl_name}-panel.conf
Source3:        %{pecl_name}.conf.php

# Restore APC serializers ABI (merged upstream)
# https://github.com/krakjoe/apcu/pull/25
Patch0:         %{pecl_name}-git.patch

License:        PHP
Group:          Development/Languages
URL:            http://pecl.php.net/package/APCu
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires:  %{?scl_prefix}%{php_base}-devel
BuildRequires:  %{?scl_prefix}%{php_base}-pear
BuildRequires:  pcre-devel

Requires(post): %{__pecl}
Requires(postun): %{__pecl}

Requires:       %{?scl_prefix}%{php_base}(zend-abi) = %{php_zend_api}
Requires:       %{?scl_prefix}%{php_base}(api) = %{php_core_api}


Conflicts:      %{?scl_prefix}php-apcu < 4.0.0-1
Provides:       %{?scl_prefix}php-apcu = %{version}
Provides:       %{?scl_prefix}php-apcu%{?_isa} = %{version}
Provides:       %{?scl_prefix}php-pecl(apcu) = %{version}
Provides:       %{?scl_prefix}php-pecl(apcu)%{?_isa} = %{version}

Provides:       %{?scl_prefix}%{php_base}-apcu = %{version}
Provides:       %{?scl_prefix}%{php_base}-apcu%{?_isa} = %{version}
Provides:       %{?scl_prefix}%{php_base}-pecl(apcu) = %{version}
Provides:       %{?scl_prefix}%{php_base}-pecl(apcu)%{?_isa} = %{version}
%if 0%{?fedora} < 20
Conflicts:      %{?scl_prefix}php-pecl-apc < 4
%else
Obsoletes:      %{?scl_prefix}php-pecl-apc < 4
%endif
# Same provides than APC, this is a drop in replacement
Provides:       %{?scl_prefix}php-apc = %{version}
Provides:       %{?scl_prefix}php-apc%{?_isa} = %{version}
Provides:       %{?scl_prefix}php-pecl-apc = %{version}
Provides:       %{?scl_prefix}php-pecl-apc%{?_isa} = %{version}
Provides:       %{?scl_prefix}php-pecl(APC) = %{version}
Provides:       %{?scl_prefix}php-pecl(APC)%{?_isa} = %{version}


Provides:       %{?scl_prefix}%{php_base}-apc = %{version}
Provides:       %{?scl_prefix}%{php_base}-apc%{?_isa} = %{version}
Provides:       %{?scl_prefix}%{php_base}-pecl-apc = %{version}
Provides:       %{?scl_prefix}%{php_base}-pecl-apc%{?_isa} = %{version}
Provides:       %{?scl_prefix}%{php_base}-pecl(APC) = %{version}
Provides:       %{?scl_prefix}%{php_base}-pecl(APC)%{?_isa} = %{version}

# Filter private shared
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}


%description
APCu is userland caching: APC stripped of opcode caching in preparation
for the deployment of Zend OPcache as the primary solution to opcode
caching in future versions of PHP.

APCu has a revised and simplified codebase, by the time the PECL release
is available, every part of APCu being used will have received review and
where necessary or appropriate, changes.

Simplifying and documenting the API of APCu completely removes the barrier
to maintenance and development of APCu in the future, and additionally allows
us to make optimizations not possible previously because of APC's inherent
complexity.

APCu only supports userland caching (and dumping) of variables, providing an
upgrade path for the future. When O+ takes over, many will be tempted to use
3rd party solutions to userland caching, possibly even distributed solutions;
this would be a grave error. The tried and tested APC codebase provides far
superior support for local storage of PHP variables.


%package devel
Summary:       APCu developer files (header)
Group:         Development/Libraries
Requires:      %{name}%{?_isa} = %{version}-%{release}
Requires:      %{?scl_prefix}%php_base}-devel%{?_isa}
%if 0%{?fedora} < 20
Conflicts:      %{?scl_prefix}php-pecl-apc-devel < 4
%else
Conflicts:      %{?scl_prefix}php-pecl-apc-devel < 4
Provides:       %{?scl_prefix}php-pecl-apc-devel = %{version}-%{release}
Provides:       %{?scl_prefix}php-pecl-apc-devel%{?_isa} = %{version}-%{release}
Provides:       %{?scl_prefix}%{php_base}-pecl-apc-devel = %{version}-%{release}
Provides:       %{?scl_prefix}%{php_base}-pecl-apc-devel%{?_isa} = %{version}-%{release}
%endif

%description devel
These are the files needed to compile programs using APCu.


#%package -n %{?scl_prefix}apcu-panel
%package -n %{?scl_prefix}%{php_base}-pecl-apcu-panel
Summary:       APCu control panel
Group:         Applications/Internet
BuildArch:     noarch
Requires:      %{name} = %{version}-%{release}
Requires:      %{?scl_prefix}mod_php, httpd, %{?scl_prefix}php-gd
%if 0%{?fedora} < 20
Conflicts:      %{?scl_prefix}apc-panel < 4
%else
Conflicts:      %{?scl_prefix}apc-panel < 4
Provides:       %{?scl_prefix}apc-panel = %{version}-%{release}
Provides:       %{?scl_prefix}%{php_base}-pecl-apc-panel = %{version}-%{release}
%endif

%description  -n %{?scl_prefix}%{php_base}-pecl-apcu-panel
This package provides the APCu control panel, with Apache
configuration, available on http://localhost/apcu-panel/


%prep
%setup -qc
mv %{pecl_name}-%{version} NTS

cd NTS
%patch0 -p1 -b .serializers
rm -f apc_serializer.h.serializers

# Sanity check, really often broken
extver=$(sed -n '/#define PHP_APC_VERSION/{s/.* "//;s/".*$//;p}' php_apc.h)
if test "x${extver}" != "x%{version}"; then
   : Error: Upstream extension version is ${extver}, expecting %{version}.
   exit 1
fi
cd ..

%if %{with_zts}
# duplicate for ZTS build
cp -pr NTS ZTS
%endif


%build
cd NTS
%{_bindir}/phpize
%configure --with-php-config=%{_bindir}/php-config
make %{?_smp_mflags}

%if %{with_zts}
cd ../ZTS
%{_bindir}/zts-phpize
%configure --with-php-config=%{_bindir}/zts-php-config
make %{?_smp_mflags}
%endif


%install
# Install the NTS stuff
make -C NTS install INSTALL_ROOT=%{buildroot}
install -D -m 644 %{SOURCE1} %{buildroot}%{php_inidir}/%{pecl_name}.ini

# Install the ZTS stuff
%if %{with_zts}
make -C ZTS install INSTALL_ROOT=%{buildroot}
install -D -m 644 %{SOURCE1} %{buildroot}%{php_ztsinidir}/%{pecl_name}.ini
%endif

# Install the package XML file
install -D -m 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

# Install the Control Panel
# Pages
install -d -m 755 %{buildroot}%{_datadir}/%{?scl_prefix}apcu-panel
install -D -m 644 -p NTS/apc.php  \
        %{buildroot}%{_datadir}/%{?scl_prefix}apcu-panel/index.php
sed -e s:apc.conf.php:%{_sysconfdir}/%{?scl_prefix}apcu-panel/conf.php:g \
    -i  %{buildroot}%{_datadir}/%{?scl_prefix}apcu-panel/index.php
# Apache config
install -D -m 644 -p %{SOURCE2} \
        %{buildroot}%{_root_sysconfdir}/httpd/conf.d/%{?scl_prefix}apcu-panel.conf
# fix path (only needed in SCL)
sed -e 's:apcu-panel:%{?scl_prefix}apcu-panel:g' \
    -e 's:/usr/share:%{_datadir}:' \
    -i  %{buildroot}%{_root_sysconfdir}/httpd/conf.d/%{?scl_prefix}apcu-panel.conf
# Panel config
install -D -m 644 -p %{SOURCE3} \
        %{buildroot}%{_sysconfdir}/%{?scl_prefix}apcu-panel/conf.php


%check
cd NTS

# Check than both extensions are reported (BC mode)
%{_bindir}/php -n -d extension_dir=modules -d extension=apcu.so -m | grep 'apcu'
%{_bindir}/php -n -d extension_dir=modules -d extension=apcu.so -m | grep 'apc$'

# Upstream test suite
TEST_PHP_EXECUTABLE=%{_bindir}/php \
TEST_PHP_ARGS="-n -d extension_dir=$PWD/modules -d extension=%{pecl_name}.so" \
NO_INTERACTION=1 \
REPORT_EXIT_STATUS=1 \
%{_bindir}/php -n run-tests.php

%if %{with_zts}
cd ../ZTS

%{__ztsphp}    -n -d extension_dir=modules -d extension=apcu.so -m | grep 'apcu'
%{__ztsphp}    -n -d extension_dir=modules -d extension=apcu.so -m | grep 'apc$'

TEST_PHP_EXECUTABLE=%{__ztsphp} \
TEST_PHP_ARGS="-n -d extension_dir=$PWD/modules -d extension=%{pecl_name}.so" \
NO_INTERACTION=1 \
REPORT_EXIT_STATUS=1 \
%{__ztsphp} -n run-tests.php
%endif


%post
%{pecl_install} %{pecl_xmldir}/%{name}.xml >/dev/null || :


%postun
if [ $1 -eq 0 ] ; then
    %{pecl_uninstall} %{pecl_name} >/dev/null || :
fi


%files
%doc NTS/{NOTICE,LICENSE,README.md}
%{pecl_xmldir}/%{name}.xml

%config(noreplace) %{php_inidir}/%{pecl_name}.ini
%{php_extdir}/%{pecl_name}.so

%if %{with_zts}
%{php_ztsextdir}/%{pecl_name}.so
%config(noreplace) %{php_ztsinidir}/%{pecl_name}.ini
%endif

%files devel
%{php_incldir}/ext/%{pecl_name}
%if %{with_zts}
%{php_ztsincldir}/ext/%{pecl_name}
%endif

%files -n %{?scl_prefix}%{php_base}-pecl-apcu-panel
%defattr(-,root,root,-)
# Need to restrict access, as it contains a clear password
%attr(750,apache,root) %dir %{_sysconfdir}/%{?scl_prefix}apcu-panel
%config(noreplace) %{_sysconfdir}/%{?scl_prefix}apcu-panel/conf.php
%config(noreplace) %{_root_sysconfdir}/httpd/conf.d/%{?scl_prefix}apcu-panel.conf
%{_datadir}/%{?scl_prefix}apcu-panel


%changelog
* Fri Aug 30 2013 Ben Harper <ben.harper@rackspace.com> - 4.0.1-4.ius
- porting from EPEL 

* Sat Jul 27 2013 Remi Collet <remi@fedoraproject.org> - 4.0.1-3
- restore APC serializers ABI (patch merged upstream)

* Mon Jul 15 2013 Remi Collet <rcollet@redhat.com> - 4.0.1-2
- adapt for SCL

* Tue Apr 30 2013 Remi Collet <remi@fedoraproject.org> - 4.0.1-1
- Update to 4.0.1
- add missing scriptlet
- fix Conflicts

* Thu Apr 25 2013 Remi Collet <remi@fedoraproject.org> - 4.0.0-2
- fix segfault when used from command line

* Wed Mar 27 2013 Remi Collet <remi@fedoraproject.org> - 4.0.0-1
- first pecl release
- rename from php-apcu to php-pecl-apcu

* Tue Mar 26 2013 Remi Collet <remi@fedoraproject.org> - 4.0.0-0.4.git4322fad
- new snapshot (test before release)

* Mon Mar 25 2013 Remi Collet <remi@fedoraproject.org> - 4.0.0-0.3.git647cb2b
- new snapshot with our pull request
- allow to run test suite simultaneously on 32/64 arch
- build warning free

* Mon Mar 25 2013 Remi Collet <remi@fedoraproject.org> - 4.0.0-0.2.git6d20302
- new snapshot with full APC compatibility

* Sat Mar 23 2013 Remi Collet <remi@fedoraproject.org> - 4.0.0-0.1.git44e8dd4
- initial package, version 4.0.0
