%define hash a3fa349173c9
%define longhash a3fa349173c9ae2d960522e78f9f8250cbb4d874
%define revision 6160

Name:           quodlibet
Version:        3.0.99
Release:        2.%{revision}.%{hash}%{?dist}
Summary:        A music management program

%if 0%{?suse_version}
Group:          Productivity/Multimedia/Sound/Players
%else
# fedora
Group:          Applications/Multimedia
%endif
License:        GPL-2.0
URL:            http://code.google.com/p/quodlibet/
Source0:        http://quodlibet.googlecode.com/archive/%{longhash}.zip

BuildArch:      noarch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  gettext
BuildRequires:  intltool
BuildRequires:  desktop-file-utils
BuildRequires:  python >= 2.6
# needed for gtk-update-icon-cache
BuildRequires:  gtk2 >= 2.6.0
BuildRequires:  unzip

%if 0%{?fedora}
# needed for py_byte_compile
BuildRequires:  python3-devel
%endif

Requires:       exfalso = %{version}-%{release}

Requires:       python-feedparser
Requires:       media-player-info
Requires:       udisks
Requires:       libgpod

%if 0%{?suse_version}
Requires:       dbus-1-python
Requires:       gstreamer >= 1.0
Requires:       gstreamer-plugins-base >= 1.0
Requires:       gstreamer-plugins-good >= 1.0
%else
# fedora
Requires:       dbus-python
Requires:       gstreamer1
Requires:       gstreamer1-plugins-base
Requires:       gstreamer1-plugins-good
%endif


%description
Quod Libet is a music management program. It provides several different ways
to view your audio library, as well as support for Internet radio and
audio feeds. It has extremely flexible metadata tag editing and searching
capabilities.
Supported file formats include Ogg Vorbis, MP3, FLAC, MOD/XM/IT, Musepack,
Wavpack, and MPEG-4 AAC.


%package -n exfalso
Summary: Tag editor for various music files
Group: Applications/Multimedia

Requires:       python >= 2.6
Requires:       python-mutagen >= 1.14
Requires:       gtk3 >= 3.2

%if 0%{?fedora}
Requires:       pygobject3 >= 3.2
Requires:       python-CDDB
Requires:       python-musicbrainz2
%else
# suse
Requires:       python-gobject >= 3.2
Requires:       python-gobject-cairo >= 3.2
%endif

%description -n exfalso
Ex Falso is a tag editor with the same tag editing interface as Quod Libet,
but it does not play files.
Supported file formats include Ogg Vorbis, MP3, FLAC, MOD/XM/IT, Musepack,
Wavpack, and MPEG-4 AAC.

%prep
%setup -q -n quodlibet-%{hash}

%build
cd quodlibet
%{__python} setup.py build

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{python_sitelib}/quodlibet/
cp -R plugins %{buildroot}%{python_sitelib}/quodlibet/

%if 0%{?fedora}
%py_byte_compile %{__python} %{buildroot}%{python_sitelib}/quodlibet/plugins
%endif

%if 0%{?suse_version}
%py_compile %{buildroot}%{python_sitelib}/quodlibet/plugins
%endif

cd quodlibet
python setup.py install --root=%{buildroot} --prefix=%{_prefix}

# leave vendor for fedora to keep links alive
%if 0%{?fedora}
desktop-file-install --vendor fedora                            \
        --dir %{buildroot}%{_datadir}/applications              \
        --delete-original                                       \
        %{buildroot}%{_datadir}/applications/quodlibet.desktop
desktop-file-install --vendor fedora                            \
        --dir %{buildroot}%{_datadir}/applications              \
        --delete-original                                       \
        %{buildroot}%{_datadir}/applications/exfalso.desktop
%else
desktop-file-install                                            \
        --dir %{buildroot}%{_datadir}/applications              \
        --delete-original                                       \
        %{buildroot}%{_datadir}/applications/quodlibet.desktop
desktop-file-install                                            \
        --dir %{buildroot}%{_datadir}/applications              \
        --delete-original                                       \
        %{buildroot}%{_datadir}/applications/exfalso.desktop
%endif

%{find_lang} quodlibet

%clean
rm -rf %{buildroot}

%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files
%defattr(-,root,root,-)
%{_bindir}/quodlibet
%if 0%{?fedora}
%{_datadir}/applications/fedora-quodlibet.desktop
%else
%{_datadir}/applications/quodlibet.desktop
%endif
%{_datadir}/pixmaps/quodlibet.png
%{_datadir}/icons/hicolor/64x64/apps/quodlibet.png
%{_datadir}/icons/hicolor/scalable/apps/quodlibet.svg
%if 0%{?suse_version}
%dir %{_datadir}/gnome-shell
%dir %{_datadir}/gnome-shell/search-providers
%endif
%{_datadir}/gnome-shell/search-providers/quodlibet-search-provider.ini
%{_mandir}/man1/quodlibet.1*


%files -n exfalso -f quodlibet/%{name}.lang
%defattr(-,root,root,-)
%doc quodlibet/COPYING quodlibet/NEWS quodlibet/README
%{_bindir}/exfalso
%{_bindir}/operon
%if 0%{?fedora}
%{_datadir}/applications/fedora-exfalso.desktop
%else
%{_datadir}/applications/exfalso.desktop
%endif
%{_datadir}/pixmaps/exfalso.png
%{_datadir}/icons/hicolor/64x64/apps/exfalso.png
%{_datadir}/icons/hicolor/scalable/apps/exfalso.svg
%{_mandir}/man1/exfalso.1*
%{_mandir}/man1/operon.1*
%{python_sitelib}/quodlibet/
%{python_sitelib}/quodlibet-*.egg-info

%changelog
* Fri Dec  7 2012 Christoph Reiter <reiter.christoph@gmail.com>
- unstable build

* Mon Jul 30 2012 Johannes Lips <hannes@fedoraproject.org> - 2.4.1-1
- Update to recent upstream release 2.4.1