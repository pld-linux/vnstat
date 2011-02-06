Summary:	Console-based network traffic monitor
Summary(pl.UTF-8):	Konsolowe narzędzie do monitorowania ruchu sieciowego
Name:		vnstat
Version:	1.10
Release:	1
License:	GPL v2
Group:		Daemons
Source0:	http://humdi.net/vnstat/%{name}-%{version}.tar.gz
# Source0-md5:	95421d968689130590348ceb80ff74a8
Source1:	%{name}.sysconfig
Source2:	%{name}.cron
Source3:	%{name}-cron
Source4:	%{name}-report
URL:		http://humdi.net/vnstat/
BuildRequires:	rpmbuild(macros) >= 1.202
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires:	crondaemon
Requires:	smtpdaemon
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

# disable maximum bandwidth setting
%{__sed} -i -e "s,MaxBandwidth 100,MaxBandwidth 0,g" cfg/vnstat.conf

%build
%{__make} \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_sbindir},%{_mandir}/man1}
install -d $RPM_BUILD_ROOT{%{_localstatedir}/lib/%{name},%{_sysconfdir}/{cron.d,sysconfig}}
install -p man/vnstat.1 $RPM_BUILD_ROOT%{_mandir}/man1
install -p src/vnstat $RPM_BUILD_ROOT%{_bindir}
install -p cfg/vnstat.conf $RPM_BUILD_ROOT%{_sysconfdir}
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/%{name}
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/cron.d/%{name}
install %{SOURCE3} $RPM_BUILD_ROOT%{_sbindir}
install %{SOURCE4} $RPM_BUILD_ROOT%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 195 vnstat
%useradd -u 195 -g 195 vnstat

%postun
if [ "$1" = 0 ]; then
	%userremove vnstat
	%groupremove vnstat
fi

%files
%defattr(644,root,root,755)
%doc CHANGES COPYING FAQ README INSTALL
%config(noreplace) %{_sysconfdir}/%{name}.conf
%config(noreplace) /etc/cron.d/%{name}
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}
%{_mandir}/man1/*
%attr(755,root,root) %{_bindir}/%{name}
%attr(755,root,root) %{_bindir}/%{name}-report
%attr(755,root,root) %{_sbindir}/%{name}-cron
%attr(750,vnstat,vnstat)%{_localstatedir}/lib/%{name}
