# TODO: add SysV init file?

Summary:	Console-based network traffic monitor
Summary(pl.UTF-8):	Konsolowe narzędzie do monitorowania ruchu sieciowego
Name:		vnstat
Version:	1.15
Release:	1
License:	GPL v2
Group:		Daemons
Source0:	http://humdi.net/vnstat/%{name}-%{version}.tar.gz
# Source0-md5:	351051ef3005e3ca99123eec07ac0a7d
Source1:	%{name}.sysconfig
Source2:	%{name}.cron
Source3:	%{name}-cron
Source4:	%{name}-report
Source5:	%{name}.service
Source6:	%{name}.tmpfiles
URL:		http://humdi.net/vnstat/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	rpmbuild(macros) >= 1.671
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires(post,preun,postun):	systemd-units >= 38
Requires:	crondaemon
Requires:	smtpdaemon
Requires:	systemd-units >= 38
Provides:	group(vnstat)
Provides:	user(vnstat)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
vnStat is a console-based network traffic monitor that keeps a log of
daily network traffic for the selected interface(s). vnStat isn't a
packet sniffer. The traffic information is analyzed from the
/proc-filesystem.

%description -l pl.UTF-8
vnStat to konsolowe narzędzie do monitorowania ruchu sieciowego, które
przechowuje zapis dziennego ruchu dla wybranych interfejsów. vnStat
nie jest programem do posłuchu pakietów. Ruch sieciowyc jest
analizowany na podstawie informacji z systemu plików /proc.

%prep
%setup -q

%build
%{__aclocal}
%{__autoconf}
%{__automake}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_localstatedir}/{lib,log}/%{name} \
	$RPM_BUILD_ROOT%{_sysconfdir}/{cron.d,sysconfig} \
	$RPM_BUILD_ROOT{%{systemdtmpfilesdir},%{systemdunitdir}} \
	$RPM_BUILD_ROOT/var/run/%{name}
cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/%{name}
cp -p %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/cron.d/%{name}
cp -p %{SOURCE3} $RPM_BUILD_ROOT%{_sbindir}
cp -p %{SOURCE4} $RPM_BUILD_ROOT%{_bindir}
cp -p %{SOURCE5} $RPM_BUILD_ROOT%{systemdunitdir}/vnstat.service
cp -p %{SOURCE6} $RPM_BUILD_ROOT%{systemdtmpfilesdir}/vnstat.conf

touch $RPM_BUILD_ROOT/var/log/%{name}/%{name}.log

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 195 vnstat
%useradd -u 195 -g 195 vnstat

%post
%systemd_post vnstat.service

%preun
%systemd_preun vnstat.service

%postun
if [ "$1" = 0 ]; then
	%userremove vnstat
	%groupremove vnstat
fi
%systemd_reload

%files
%defattr(644,root,root,755)
%doc CHANGES COPYING FAQ README INSTALL
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}.conf
%config(noreplace) %verify(not md5 mtime size) /etc/cron.d/%{name}
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}
%attr(755,root,root) %{_bindir}/%{name}
%attr(755,root,root) %{_bindir}/%{name}-report
%attr(755,root,root) %{_sbindir}/%{name}-cron
%attr(755,root,root) %{_sbindir}/vnstatd
%attr(750,vnstat,vnstat)%{_localstatedir}/lib/%{name}
%{systemdunitdir}/%{name}.service
%{systemdtmpfilesdir}/%{name}.conf
%attr(750,vnstat,vnstat) %dir /var/run/%{name}
%attr(750,vnstat,vnstat) %dir /var/log/%{name}
%attr(640,vnstat,vnstat) %ghost /var/log/%{name}/%{name}.log
%{_mandir}/man1/vnstat.1*
%{_mandir}/man1/vnstatd.1*
%{_mandir}/man5/vnstat.conf.5*
