Summary:	Console-based network traffic monitor
Name:		vnstat
Version:	1.6
Release:	1
License:	GPL v2
Group:		Daemons
URL:		http://humdi.net/vnstat/
Source0:	http://humdi.net/vnstat/%{name}-%{version}.tar.gz
Requires(pre):	/usr/sbin/useradd
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
vnStat is a console-based network traffic monitor that keeps a log of
daily network traffic for the selected interface(s). vnStat isn't a
packet sniffer. The traffic information is analyzed from the
/proc-filesystem, so vnStat can be used without root permissions. See
the webpage for few 'screenshots'.

%prep
%setup -q

# disable maximum bandwidth setting
%{__sed} -i -e "s,MaxBandwidth 100,MaxBandwidth 0,g" cfg/vnstat.conf

%build
%{__make} \
	CFLAGS="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
%{__rm} -rf $RPM_BUILD_ROOT
%{__mkdir_p} $RPM_BUILD_ROOT%{_bindir}
%{__mkdir_p} $RPM_BUILD_ROOT%{_sbindir}
%{__mkdir_p} $RPM_BUILD_ROOT%{_mandir}/man1
%{__mkdir_p} $RPM_BUILD_ROOT%{_localstatedir}/lib/%{name}
%{__mkdir_p} $RPM_BUILD_ROOT%{_sysconfdir}/cron.d
%{__mkdir_p} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig

install -p man/vnstat.1 $RPM_BUILD_ROOT%{_mandir}/man1
install -p src/vnstat $RPM_BUILD_ROOT%{_bindir}
install -p cfg/vnstat.conf $RPM_BUILD_ROOT%{_sysconfdir}

%{__cat} >> $RPM_BUILD_ROOT%{_sysconfdir}/cron.d/%{name} << END
MAILTO=root
# to enable interface monitoring via vnstat remove comment on next line
# */5 * * * *  vnstat %{_sbindir}/%{name}.cron
END

%{__cat} >> $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/%{name} << END
# see also: vnstat(1)
#
# starting with vnstat-1.6 vnstat can also be
# configured via %{_sysconfdir}/vnstat.conf
#
# the following sets vnstat up to monitor eth0
VNSTAT_OPTIONS="-u -i eth0"
END

%{__cat} >> $RPM_BUILD_ROOT%{_sbindir}/%{name}.cron << END
#!/bin/bash
# this script (%{_sbindir}/%{name}.cron) reads %{_sysconfdir}/sysconfig/%{name}
# to start %{_bindir}/%{name}.
# example for %{_sysconfdir}/sysconfig/%{name}:
# VNSTAT_OPTIONS="-u -i eth0"
# see also: vnstat(1)

VNSTAT_CONF=%{_sysconfdir}/sysconfig/%{name}

if [ ! -f $VNSTAT_CONF ]; then
	exit 0
fi

. \$VNSTAT_CONF

%{_bindir}/%{name} \$VNSTAT_OPTIONS
END

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%pre
%{_sbindir}/useradd -r -s /sbin/nologin -d %{_localstatedir}/lib/%{name} \
	-M -c "vnStat user" %{name} > /dev/null 2>&1 || :

%files
%defattr(644,root,root,755)
%doc CHANGES COPYING FAQ README INSTALL cron pppd
%config(noreplace) %{_sysconfdir}/%{name}.conf
%config(noreplace) /etc/cron.d/%{name}
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}
%{_mandir}/man1/*
%attr(755,root,root) %{_bindir}/%{name}
%attr(755,root,root)%{_sbindir}/%{name}.cron
%attr(-,vnstat,vnstat)%{_localstatedir}/lib/%{name}
