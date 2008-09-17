%define topver	1.3

Summary:	An authoritative and recursive DNS server made with security in mind
Name:		maradns
Version:	1.3.07.09
Release:	%{mkrel 2}
License:	BSD
Group:		System/Servers
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
URL:		http://www.maradns.org
Source0:	http://www.maradns.org/download/%{topver}/%{version}/%{name}-%{version}.tar.lzma
Source1:	http://www.maradns.org/download/%{topver}/%{version}/%{name}-%{version}.tar.lzma.sha.asc
Patch0:		maradns-1.3.07.09-install.patch
Patch1:		maradns-1.3.07.09-initscript.patch
Patch2:		maradns-1.3.07.09-mararc_examples.patch
Requires(post):	rpm-helper

%description
MaraDNS is an authoritative and recursive DNS server made with
security in mind. More information is at http://www.maradns.org.

%prep
%setup -q
%patch0 -p1 -b .path
%patch1 -p1
%patch2 -p1

%build
%make FLAGS="%{optflags}"

%install
 [ -n "%{buildroot}" -a "%{buildroot}" != / ] \
  && rm -rf %{buildroot}/

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

# remove unwanted %doc files
rm doc/en/Makefile \
	doc/en/*.html \
	doc/en/examples/Makefile
rm -r doc/en/man \
	doc/en/misc \
	doc/en/pdf \
	doc/en/source
rm -r doc/pt_br

%clean
 [ -n "%{buildroot}" -a "%{buildroot}" != / ] \
  && rm -rf %{buildroot}/

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
%{_sbindir}/%{name}
%{_sbindir}/zoneserver
%{_sbindir}/duende
%{_bindir}/fetchzone
%{_bindir}/getzone
%{_bindir}/askmara
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man8/*
%dir %{_sysconfdir}/%{name}/logger
%config(noreplace) %{_sysconfdir}/%{name}/db.example.net
%config(noreplace) %{_sysconfdir}/%{name}/mararc*
%attr(755,root,root) %{_sysconfdir}/rc.d/init.d/%{name}*
%dir %{_logdir}/%{name}

