%{!?mdkversion:%define notmdk}
%{!?_logdir:%global _logdir %{_var}/log}
%define beta rc1
%define		_localstatedir	%{_var}/lib

Name:		devmon
Version:	0.3.0
Release:	%mkrel 0%{?beta:.%beta.}
Summary:	SNMP Device Monitoring for Hobbit/BigBrother
License:	GPL
Group:		Monitoring
URL:		http://devmon.sf.net
Source:		http://prdownloads.sourceforge.net/devmon/devmon-%{version}%{?beta:-%beta}.tar.gz
Patch:		devmon-correct-paths.patch
BuildArch:	noarch
%if %{!?notmdk:1}%{?notmdk:0}
Requires(pre):	rpm-helper
%endif
BuildRoot:	%{_tmppath}/%{name}-%{version}-root
Requires:	devmon-templates >= 20080206

%description
Devmon is a device monitoring script which works in tandem with the
Hobbit/BigBrother monitoring suites. It queries remote hosts via SNMP, applies
user-defined logic and thresholds to the acquired data, and submits status and
alarms to a display server.

%prep
%setup -q -n %{name}-%{version}%{?beta:-%beta}
%patch -p1 -b .mdv

%build

%install
rm -Rf %{buildroot}
install -d %{buildroot}/%{_datadir}/%{name} 
install -d %{buildroot}/%{_sysconfdir}/logrotate.d %{buildroot}/%{_initrddir}
install -d %{buildroot}/%{_localstatedir}/%{name} %{buildroot}/%{_var}/run/%{name}
install -d %{buildroot}/%{_logdir}/%{name}
install -d %{buildroot}/%{_localstatedir}/%{name}
cp -a modules %{buildroot}/%{_datadir}/%{name}
install -m755 devmon %{buildroot}/%{_datadir}/%{name}
install -m 640 devmon.cfg %{buildroot}/%{_sysconfdir}
install -m 755 extras/devmon.initd.redhat %{buildroot}/%{_initrddir}/devmon

cat << EOF > %{buildroot}/%{_sysconfdir}/logrotate.d/%{name}
/var/log/devmon/devmon.log {
    notifempty
    missingok
    postrotate
        /sbin/service %{name} condrestart 2> /dev/null > /dev/null || true
    endscript
}
EOF

%clean
rm -Rf %{buildroot}

%pre
%_pre_useradd %{name} %{_localstatedir}/%{name} /bin/false

%post
%_post_service %{name}

%preun
%_preun_service %{name}

%postun
%_postun_userdel %{name}

%files
%defattr(-,root,root)
%{_datadir}/%{name}
%attr(,640,root,devmon) %config(noreplace) %{_sysconfdir}/devmon.cfg
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%config %{_initrddir}/%{name}
%attr(755,devmon,devmon) %dir %{_logdir}/%{name}
%attr(755,devmon,devmon) %dir %{_var}/run/%{name}
%attr(755,devmon,devmon) %dir %{_localstatedir}/%{name}

%doc docs/* README CHANGELOG extras/devmon.db
