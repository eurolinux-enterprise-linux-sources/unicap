%define _use_internal_dependency_generator 0
%{expand:%%define prev__find_provides %{__find_provides}}
%define __find_provides sh %{SOURCE1} %{prev__find_provides}
%{expand:%%define prev__find_requires %{__find_requires}}
%define __find_requires sh %{SOURCE1} %{prev__find_requires}

Summary:	Library to access different kinds of (video) capture devices
Name:		unicap
Version:	0.9.5
Release:	7%{?dist}
License:	GPLv2+
Group:		System Environment/Libraries
URL:		http://www.unicap-imaging.org/
Source0:	http://www.unicap-imaging.org/downloads/%{name}-%{version}.tar.gz
Source1:	unicap-filter.sh
BuildRequires:	intltool, /usr/bin/perl, perl(XML::Parser), gettext
BuildRequires:	glib2-devel, gtk2-devel, pango-devel, libtheora-devel, libXv-devel
BuildRequires:	libpng-devel, libX11-devel, libICE-devel
%ifnarch s390 s390x
BuildRequires:	libraw1394-devel >= 1.1.0
%endif
BuildRequires:	libogg-devel, libvorbis-devel, libXext-devel, alsa-lib-devel
BuildRequires:	libv4l-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# bz #635644
Patch1: unicap-0.9.5-bz635644.patch

# bz #635645
Patch2: unicap-0.9.5-bz635645.patch

# bz #581187
Provides:	libucil		= %{version}-%{release}
Provides:	libunicap	= %{version}-%{release}
Provides:	libunicapgtk	= %{version}-%{release}

%description
Unicap provides a uniform interface to video capture devices. It allows
applications to use any supported video capture device via a single API.
The included ucil library provides easy to use functions to render text
and graphic overlays onto video images.

%package devel
Summary:	Development files for the unicap library
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}, pkgconfig

# bz #581187
Provides:	libucil-devel		= %{version}-%{release}
Provides:	libunicap-devel		= %{version}-%{release}
Provides:	libunicapgtk-devel	= %{version}-%{release}

%description devel
The unicap-devel package includes header files and libraries necessary for
for developing programs which use the unicap, unicapgtk and ucil library. It
contains the API documentation of the library, too.

%prep
%setup -q
%patch1 -p1
%patch2 -p1

%build
%configure --disable-rpath --disable-gtk-doc --enable-libv4l
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

# Don't install any static .a and libtool .la files
rm -f $RPM_BUILD_ROOT%{_libdir}/{,unicap2/cpi/}*.{a,la}

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(-,root,root)
%doc AUTHORS ChangeLog COPYING README
%{_libdir}/*.so.*
%{_libdir}/unicap2

%files devel
%defattr(-,root,root)
%doc examples
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/%{name}
%{_datadir}/gtk-doc/html/*

%changelog
* Fri Aug 05 2011 Kamil Dudka <kdudka@redhat.com> - 0.9.5-7
- do not mistakenly drop the dependency on libv4l2.so.0 (#728473)

* Fri Aug 05 2011 Kamil Dudka <kdudka@redhat.com> - 0.9.5-6
- do not use gtk-doc, use the documentation provided by upstream (#658059)

* Tue Jun 28 2011 Kamil Dudka <kdudka@redhat.com> - 0.9.5-5
- fix provides for libunicap, libunicapgtk and libucil (#612693)
- fix SIGSEGV in ucil_alsa_fill_audio_buffer (#635644)
- check return value of theora_encode_init() (#635645)
- avoid a multilib conflict on unicap-devel (#658059)

* Mon Apr 12 2010 Kamil Dudka <kdudka@redhat.com> - 0.9.5-4
- declare provides for libunicap, libunicapgtk and libucil (#581187)

* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 0.9.5-3.1
- Rebuilt for RHEL 6

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jun 18 2009 Dan Horak <dan[at]danny.cz> 0.9.5-2
- don't require libraw1394 on s390/s390x

* Sun May 03 2009 Robert Scheck <robert@fedoraproject.org> 0.9.5-1
- Upgrade to 0.9.5

* Mon Feb 23 2009 Robert Scheck <robert@fedoraproject.org> 0.9.3-2
- Rebuild against gcc 4.4 and rpm 4.6

* Mon Oct 13 2008 Robert Scheck <robert@fedoraproject.org> 0.9.3-1
- Upgrade to 0.9.3 (#466825, thanks to Hans de Goede)
- Enabled libv4l support for the new gspca kernel driver

* Sat Aug 09 2008 Robert Scheck <robert@fedoraproject.org> 0.2.23-4
- Rebuild to get missing dependencies back (#443015, #458527)

* Tue Aug 05 2008 Robert Scheck <robert@fedoraproject.org> 0.2.23-3
- Filter the unicap plugins which overlap with libv4l libraries

* Wed Jul 22 2008 Robert Scheck <robert@fedoraproject.org> 0.2.23-2
- Rebuild for libraw1394 2.0.0

* Mon May 19 2008 Robert Scheck <robert@fedoraproject.org> 0.2.23-1
- Upgrade to 0.2.23
- Corrected packaging of cpi/*.so files (thanks to Arne Caspari)

* Sat May 17 2008 Robert Scheck <robert@fedoraproject.org> 0.2.22-1
- Upgrade to 0.2.22 (#446021)

* Sat Feb 16 2008 Robert Scheck <robert@fedoraproject.org> 0.2.19-3
- Added patch to correct libdir paths (thanks to Ralf Corsepius)

* Mon Feb 04 2008 Robert Scheck <robert@fedoraproject.org> 0.2.19-2
- Changes to match with Fedora Packaging Guidelines (#431381)

* Mon Feb 04 2008 Robert Scheck <robert@fedoraproject.org> 0.2.19-1
- Upgrade to 0.2.19
- Initial spec file for Fedora and Red Hat Enterprise Linux
