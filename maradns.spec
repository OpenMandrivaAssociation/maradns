%define topver	2.0
%define deadwoodversion 3.0.02

Summary:	An authoritative and recursive DNS server made with security in mind
Name:		maradns
Version:	2.0.02
Release:	%mkrel 1
License:	BSD
Group:		System/Servers
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
URL:		http://www.maradns.org
Source0:	http://www.maradns.org/download/%{topver}/%{version}/%{name}-%{version}.tar.bz2
Source1:	deadwood.init
Patch0:		maradns-1.3.07.09-install.patch
Patch1:		maradns-1.3.07.09-initscript.patch
Patch2:		maradns-1.3.07.09-mararc_examples.patch
Requires(post):	rpm-helper

%description
MaraDNS is an authoritative and recursive DNS server made with
security in mind. More information is at http://www.maradns.org.

%package -n deadwood
Summary:	a fully recursive DNS cache
Version:	%{deadwoodversion}

%description -n deadwood
Deadwood is a fully recursive DNS cache. This is a DNS server with 
the following features:
 * Full support for both DNS recursion and DNS forwarding caching
 * Small size and memory footprint suitable for embedded systems
 * Simple and clean codebase
 * Secure design
 * Spoof protection: Strong cryptography used to determine the Query ID and source port
 * Ability to read and write the cache to a file
 * Dynamic cache that deletes entries not recently used
 * Ability to use expired entries in the cache when it is impossible to contact upstream DNS servers.
 * Ipv6 support can be compiled in if desired
 * Both DNS-over-UDP and DNS-over-TCP are handled by the same daemon
 * Built-in dnswall functionality

%prep
%setup -q
%patch0 -p1 -b .path
%patch1 -p1
%patch2 -p1

%build
%setup_compile_flags
%make

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{_sbindir}
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_mandir}/{man1,man5,man8}
mkdir -p %{buildroot}/%{_initrddir}
mkdir -p %{buildroot}%{_logdir}/%{name}

PREFIX="%{buildroot}%{_prefix}" make install

install -m 0644 doc/en/examples/example_authoritative_mararc.txt \
	%{buildroot}%{_sysconfdir}/%{name}/mararc.authorative
install -m 0644 doc/en/examples/example_full_mararc \
	%{buildroot}%{_sysconfdir}/%{name}/mararc.full
install -m 0644 doc/en/examples/example_recursive_mararc.txt \
	%{buildroot}%{_sysconfdir}/%{name}/mararc.recursive
install -m 0644 deadwood-%{deadwoodversion}/doc/Deadwood.1 \
	%{buildroot}%{_mandir}/man1/Deadwood.1
install -m 0644 deadwood-%{deadwoodversion}/doc/dwood3rc \
	%{buildroot}/%{_sysconfdir}/dwood3rc
install -m 0755 %{SOURCE1} %{buildroot}/%{_sysconfdir}/rc.d/init.d/deadwood

# remove unwanted doc files
rm doc/en/Makefile \
	doc/en/*.html \
	doc/en/examples/Makefile
rm -r doc/en/man \
	doc/en/misc \
	doc/en/pdf \
	doc/en/source

%clean
rm -rf %{buildroot}/

%pre
%_pre_useradd maradns /etc/maradns /bin/false
%_pre_groupadd maradns maradns
#if [ $1 = 1 ]
#	then
#	/usr/sbin/groupadd -r -g 99 maradns > /dev/null 2>&1
#	/usr/sbin/useradd -u 99 -r -d /etc/maradns -s /bin/false \
#	-c "Maradns pseudo user" -g maradns maradns  > /dev/null 2>&1
#fi

%post
%_post_service maradns

%preun
%_preun_service maradns

%postun
%_postun_userdel maradns
%_postun_groupdel maradns


%files
%defattr(-,root,root)
%doc doc/*
%attr(755,root,root) %{_sysconfdir}/rc.d/init.d/%{name}*
%dir %{_sysconfdir}/%{name}
%dir %{_sysconfdir}/%{name}/logger
%config(noreplace) %{_sysconfdir}/%{name}/db.example.net
%config(noreplace) %{_sysconfdir}/%{name}/mararc*
%{_bindir}/fetchzone
%{_bindir}/getzone
%{_bindir}/askmara
%{_sbindir}/%{name}
%{_sbindir}/zoneserver
%{_sbindir}/duende
%{_mandir}/man1/askmara.1*
%{_mandir}/man1/fetchzone.1*
%{_mandir}/man1/getzone.1*
%{_mandir}/man5/*
%{_mandir}/man8/*
%dir %{_logdir}/%{name}

%files -n deadwood
%defattr(-,root,root)
%doc deadwood-%{deadwoodversion}/doc/Deadwood.txt
%doc deadwood-%{deadwoodversion}/doc/FAQ.txt
%config(noreplace) %{_sysconfdir}/dwood3rc
%attr(755,root,root) %{_sysconfdir}/rc.d/init.d/deadwood
%{_sbindir}/Deadwood
%{_mandir}/man1/Deadwood.1*
