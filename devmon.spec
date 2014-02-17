%define beta beta1

Summary:	SNMP Device Monitoring for Hobbit/BigBrother
Name:		devmon
Version:	0.3.1
Release:	0.%{beta}.3
License:	GPLv2+
Group:		Monitoring
Url:		http://devmon.sf.net
Source0:	http://prdownloads.sourceforge.net/devmon/devmon-%{version}%{?beta:-%beta}.tar.gz
Patch0:		devmon-correct-paths.patch
Requires:	devmon-templates
Requires(pre,post,preun,postun):	rpm-helper
BuildArch:	noarch

%description
Devmon is a device monitoring script which works in tandem with the
Hobbit/BigBrother monitoring suites. It queries remote hosts via SNMP, applies
user-defined logic and thresholds to the acquired data, and submits status and
alarms to a display server.

%files
%doc docs/* README CHANGELOG extras/devmon.db extras/devmon-graph.cfg
%{_datadir}/%{name}
%attr(,640,root,devmon) %config(noreplace) %{_sysconfdir}/devmon.cfg
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%config %{_initrddir}/%{name}
%attr(755,devmon,devmon) %dir %{_logdir}/%{name}
%attr(755,devmon,devmon) %dir %{_var}/run/%{name}
%attr(755,devmon,devmon) %dir %{_localstatedir}/lib/%{name}

%pre
%_pre_useradd %{name} %{_localstatedir}/lib/%{name} /bin/false

%post
%_post_service %{name}

%preun
%_preun_service %{name}

%postun
%_postun_userdel %{name}

#----------------------------------------------------------------------------

%prep
%setup -q -n %{name}-%{version}-%{beta}
%patch0 -p1 -b .mdv

%build

%install
install -d %{buildroot}/%{_datadir}/%{name}
install -d %{buildroot}/%{_sysconfdir}/logrotate.d %{buildroot}/%{_initrddir}
install -d %{buildroot}/%{_localstatedir}/lib/%{name} %{buildroot}/%{_var}/run/%{name}
install -d %{buildroot}/%{_logdir}/%{name}
install -d %{buildroot}/%{_localstatedir}/lib/%{name}
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

