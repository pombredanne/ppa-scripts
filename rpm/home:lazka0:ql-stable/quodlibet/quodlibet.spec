Name:           quodlibet
Version:        2.4.91
Release:        1.1%{?dist}
Summary:        A music management program

%if 0%{?suse_version}
Group:          Productivity/Multimedia/Sound/Players
%else
Group:          Applications/Multimedia
%endif
License:        GPL-2.0
URL:            http://code.google.com/p/quodlibet/
Source0:        http://quodlibet.googlecode.com/files/quodlibet-%{version}.tar.gz
Source1:        http://quodlibet.googlecode.com/files/quodlibet-plugins-%{version}.tar.gz

BuildArch:      noarch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  gettext
BuildRequires:  intltool
BuildRequires:  desktop-file-utils
BuildRequires:  gtk2 >= 2.6.0
BuildRequires:  python >= 2.6
BuildRequires:  pygtk2 >= 2.16
BuildRequires:  unzip

%if 0%{?fedora}
# needed for py_byte_compile
BuildRequires:  python3-devel
%endif

Requires:       exfalso = %{version}-%{release}
Requires:       gstreamer-python >= 0.10.2
Requires:       gstreamer-plugins-good
Requires:       python-feedparser
Requires:       media-player-info
Requires:       dbus-python
Requires:       python-keybinder
Requires:       udisks

# for iPod device support
Requires:       python-gpod

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
Requires:       pygtk2 >= 2.16
Requires:       python-mutagen >= 1.14

# for CDDB plugin
Requires:       python-CDDB

# for musicbrainz plugin
Requires:       python-musicbrainz2

%description -n exfalso
Ex Falso is a tag editor with the same tag editing interface as Quod Libet,
but it does not play files.
Supported file formats include Ogg Vorbis, MP3, FLAC, MOD/XM/IT, Musepack,
Wavpack, and MPEG-4 AAC.

%prep
%setup -q

%build
%{__python} setup.py build

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{python_sitelib}/quodlibet/plugins
tar --verbose --strip-components=1 --extract --file=%{S:1} --directory=%{buildroot}%{python_sitelib}/quodlibet/plugins

%if 0%{?fedora}
%py_byte_compile %{__python} %{buildroot}%{python_sitelib}/quodlibet/plugins
%endif

%if 0%{?suse_version}
%py_compile %{buildroot}%{python_sitelib}/quodlibet/plugins
%endif

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
%{_mandir}/man1/quodlibet.1*


%files -n exfalso -f %{name}.lang
%defattr(-,root,root,-)
%doc COPYING HACKING NEWS README
%{_bindir}/exfalso
%if 0%{?fedora}
%{_datadir}/applications/fedora-exfalso.desktop
%else
%{_datadir}/applications/exfalso.desktop
%endif
%{_datadir}/pixmaps/exfalso.png
%{_datadir}/icons/hicolor/64x64/apps/exfalso.png
%{_datadir}/icons/hicolor/scalable/apps/exfalso.svg
%{_mandir}/man1/exfalso.1*
%{python_sitelib}/quodlibet/
%{python_sitelib}/quodlibet-%{version}-py*.egg-info

%changelog
* Fri Dec  7 2012 Christoph Reiter <reiter.christoph@gmail.com>
- unstable build

* Mon Jul 30 2012 Johannes Lips <hannes@fedoraproject.org> - 2.4.1-1
- Update to recent upstream release 2.4.1