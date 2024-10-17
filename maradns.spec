%define topver	1.4

Summary:	An authoritative and recursive DNS server made with security in mind
Name:		maradns
Version:	1.4.06
Release:	3
License:	BSD
Group:		System/Servers
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
URL:		https://www.maradns.org
Source0:	http://www.maradns.org/download/%{topver}/%{version}/%{name}-%{version}.tar.bz2
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
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man8/*
%dir %{_logdir}/%{name}


%changelog
* Mon Feb 28 2011 Funda Wang <fwang@mandriva.org> 1.4.06-2mdv2011.0
+ Revision: 640875
- rebuild

* Tue Feb 01 2011 Lonyai Gergely <aleph@mandriva.org> 1.4.06-1
+ Revision: 634613
- 1.4.06

* Tue Feb 01 2011 Lonyai Gergely <aleph@mandriva.org> 1.3.07.09-6
+ Revision: 634610
- Sec fix: CVE-2011-0520 - allows remote attackers to cause a denial of service (segmentation fault) and possibly execute arbitrary code via a long DNS hostname with a large number of labels, which triggers a heap-based buffer overflow.

* Mon Dec 06 2010 Oden Eriksson <oeriksson@mandriva.com> 1.3.07.09-5mdv2011.0
+ Revision: 612815
- the mass rebuild of 2010.1 packages

* Sat May 22 2010 Ahmad Samir <ahmadsamir@mandriva.org> 1.3.07.09-4mdv2010.1
+ Revision: 545708
- fix adding and removing user and group in pre and postun stages
  (reported on cooker ML)
- clean spec

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild

* Wed Sep 17 2008 Michael Scherer <misc@mandriva.org> 1.3.07.09-2mdv2009.0
+ Revision: 285431
- rebuild to fix #43089
- remove conflict with tmdns, as we no longer ship it

* Sat Sep 06 2008 Adam Williamson <awilliamson@mandriva.org> 1.3.07.09-1mdv2009.0
+ Revision: 281763
- clean file list
- use %%{name} in file list
- clean up removal of doc files
- use macros when creating directories, not hardcoded names
- s,$RPM_BUILD_ROOT,%%{buildroot}
- use MDV optflags
- rediff all patches
- include the tarball signature as a source
- clean tabs/spaces
- drop unnecessary defines
- new release 1.3.07.09

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild
    - fix no-buildroot-tag
    - fix installing with new docdir
    - kill re-definition of %%buildroot on Pixel's request
    - use %%mkrel
    - import maradns


* Mon Aug 29 2005 Marcel Pol <mpol@mandriva.org> 1.1.43-1mdk
- 1.1.43

* Wed Aug 10 2005 Marcel Pol <mpol@mandriva.org> 1.1.42-1mdk
- 1.1.42
- drop Source2,3
- update and add P0,1,2
- license is BSD now

* Mon May 31 2004 Marcel Pol <mpol@mandrake.org> 1.0.23-1mdk
- 1.0.23

* Sun Jun 01 2003 Marcel Pol <mpol@gmx.net> 1.0.18-1mdk
- 1.0.18

* Sun Apr 20 2003 Marcel Pol <mpol@gmx.net> 1.0.17-1mdk
- 1.0.17

* Wed Apr 02 2003 Marcel Pol <mpol@gmx.net> 1.0.16-1mdk
- 1.0.16

* Tue Mar 11 2003 Marcel Pol <mpol@gmx.net> 1.0.13-2mdk
- conflicts: tmdns

* Thu Feb 06 2003 Marcel Pol <mpol@gmx.net> 1.0.13-1mdk
- 1.0.13

* Fri Jan 17 2003 Marcel Pol <mpol@gmx.net> 1.0.12-1mdk
- 1.0.12
- use rpm-helper script for chkconfig

* Tue Dec 24 2002 Marcel Pol <mpol@gmx.net> 1.0.11-1mdk
- 1.0.11
- don't include all docs
- %%setup -q

* Fri Nov 15 2002 Marcel Pol <mpol@gmx.net> 1.0.09-3mdk
- whoops, change mkdirhier to mkdir -p

* Fri Nov 15 2002 Marcel Pol <mpol@gmx.net> 1.0.09-2mdk
- first Mandrake build, used specfile from original package
- split initscript into initscript and sysconfig files
- add chkconfig lines to initscript
- install 3 mararc files, and use the recursive as default
- patch1 changes timeout from 2 sec. to 6 sec.
- I simply don't understand the rpm-helper scripts for useradd/userdel
- right now recursive queries are allowed from 0.0.0.0/0, that's wise?


* Fri Nov 15 2002 Florin <florin@mandrakesoft.com> 1.0.09-1mdk
- 1.0.09

* Wed Aug 27 2002 Marcel Pol <mpol@gmx.net> 1.0.07-0.1mdk
- Mandrake build

