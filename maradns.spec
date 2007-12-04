%define name	maradns
%define version	1.1.43
%define release	 %mkrel 1

Summary:	An authoritative and recursive DNS server made with security in mind
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	BSD
Group:		System/Servers
URL:		http://www.maradns.org
Source0:	http://www.maradns.org/download/%{name}-%{version}.tar.bz2
Patch0:		maradns-1.1.42-install.patch.bz2
Patch1:		maradns-1.1.42-initscript.patch.bz2
Patch2:		maradns-1.1.42-mararc_examples.patch.bz2
BuildRoot:	%_tmppath/%{name}-buildroot
Requires(post):	rpm-helper
Conflicts:	tmdns

%description
MaraDNS is an authoritative and recursive DNS server made with 
security in mind. More information is at http://www.maradns.org.

%prep
%setup -q 
%patch0 -p1 -b .path
%patch1 -p1
%patch2 -p1

%build
%make

%install
 [ -n "${RPM_BUILD_ROOT}" -a "${RPM_BUILD_ROOT}" != / ] \
  && rm -rf ${RPM_BUILD_ROOT}/

mkdir -p $RPM_BUILD_ROOT/usr/sbin
mkdir -p $RPM_BUILD_ROOT/usr/bin
mkdir -p $RPM_BUILD_ROOT/usr/share/man/{man1,man5,man8}
mkdir -p $RPM_BUILD_ROOT/etc/rc.d/init.d
mkdir -p $RPM_BUILD_ROOT/var/log/maradns
PREFIX="$RPM_BUILD_ROOT/usr/" MAN1="$RPM_BUILD_ROOT/%{_mandir}/man1" make install
cp ${RPM_BUILD_DIR}/%{name}-%{version}/doc/en/examples/example_authoritative_mararc.txt \
	$RPM_BUILD_ROOT/etc/maradns/mararc.authorative
cp ${RPM_BUILD_DIR}/%{name}-%{version}/doc/en/examples/example_full_mararc \
	$RPM_BUILD_ROOT/etc/maradns/mararc.full
cp ${RPM_BUILD_DIR}/%{name}-%{version}/doc/en/examples/example_recursive_mararc.txt \
	$RPM_BUILD_ROOT/etc/maradns/mararc.recursive

# remove unwanted %doc files
rm $RPM_BUILD_DIR/%{name}-%{version}/doc/en/Makefile \
    $RPM_BUILD_DIR/%{name}-%{version}/doc/en/logfile \
    $RPM_BUILD_DIR/%{name}-%{version}/doc/en/*.html \
    $RPM_BUILD_DIR/%{name}-%{version}/doc/en/examples/Makefile
rm -r $RPM_BUILD_DIR/%{name}-%{version}/doc/en/man \
    $RPM_BUILD_DIR/%{name}-%{version}/doc/en/misc \
    $RPM_BUILD_DIR/%{name}-%{version}/doc/en/ps \
    $RPM_BUILD_DIR/%{name}-%{version}/doc/en/source
rm $RPM_BUILD_DIR/%{name}-%{version}/doc/fr/Makefile \
    $RPM_BUILD_DIR/%{name}-%{version}/doc/fr/faq.html \
    $RPM_BUILD_DIR/%{name}-%{version}/doc/fr/examples/Makefile \
    $RPM_BUILD_DIR/%{name}-%{version}/doc/fr/tutorial/Makefile
rm -r $RPM_BUILD_DIR/%{name}-%{version}/doc/fr/man \
    $RPM_BUILD_DIR/%{name}-%{version}/doc/fr/source


%clean
 [ -n "${RPM_BUILD_ROOT}" -a "${RPM_BUILD_ROOT}" != / ] \
  && rm -rf ${RPM_BUILD_ROOT}/

%pre
#%%_pre_groupadd maradns $1 maradns maradns
#%%_pre_useradd maradns $1 maradns "/etc/maradns" /bin/false
if [ $1 = 1 ]
	then
	/usr/sbin/groupadd -r -g 99 maradns > /dev/null 2>&1
	/usr/sbin/useradd -u 99 -r -d /etc/maradns -s /bin/false \
     -c "Maradns pseudo user" -g maradns maradns  > /dev/null 2>&1
fi

%post
%_post_service maradns

%preun
%_preun_service maradns

%postun
%_postun_userdel maradns
##/usr/sbin/userdel maradns


%files
%defattr(-,root,root)
%doc doc/*
%{_sbindir}/maradns
%{_sbindir}/zoneserver
%{_sbindir}/duende
%{_bindir}/fetchzone
%{_bindir}/getzone
%{_bindir}/askmara
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man8/*
%dir %{_sysconfdir}/maradns/logger
%config(noreplace) %{_sysconfdir}/maradns/db.example.com
%config(noreplace) %{_sysconfdir}/maradns/mararc*
%attr(755,root,root) %{_sysconfdir}/rc.d/init.d/maradns
%dir /var/log/maradns

