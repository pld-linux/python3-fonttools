#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# pytest tests

Summary:	Python tools to manipulate font files
Summary(pl.UTF-8):	Narzędzia do manipulacji na plikach fontów dla Pythona
Name:		python3-fonttools
Version:	4.56.0
Release:	1
# basic license is BSD
# FontTools includes Adobe AGL & AGLFN, which is under 3-clauses BSD license
License:	MIT, BSD
Group:		Development/Tools
#Source0Download: https://github.com/fonttools/fonttools/releases
Source0:	https://github.com/fonttools/fonttools/archive/%{version}/fonttools-%{version}.tar.gz
# Source0-md5:	5226de2f08e946a3b65e83db23c093da
URL:		https://github.com/fonttools/fonttools
%if %(locale -a | grep -q '^C\.utf8$'; echo $?)
BuildRequires:	glibc-localedb-all
%endif
BuildRequires:	python3-devel >= 1:3.4
%if %{with tests}
BuildRequires:	python3-brotli
BuildRequires:	python3-pytest >= 3.0
%endif
BuildRequires:	rpmbuild(macros) >= 1.750
%if %{with doc}
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python3-modules >= 1:3.4
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Python tools to manipulate font files.

%description -l pl.UTF-8
Narzędzia do manipulacji na plikach fontów dla Pythona.

%package apidocs
Summary:	Documentation for Python fonttools module
Summary(pl.UTF-8):	Dokumentacja modułu Pythona fonttools
Group:		Documentation

%description apidocs
Documentation for Python fonttools module.

%description apidocs -l pl.UTF-8
Dokumentacja modułu Pythona fonttools.

%prep
%setup -q -n fonttools-%{version}

%build
export LC_ALL=C.UTF-8

%py3_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTHONPATH=Lib \
%{__python3} -m pytest Tests
%endif

%if %{with doc}
PYTHONPATH=$(pwd)/build-3/lib \
%{__make} -C Doc html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

# packaged from fonttools.spec
%{__rm} -r $RPM_BUILD_ROOT{%{_bindir},%{_mandir}/man1}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%{py3_sitedir}/fontTools
%{py3_sitedir}/fonttools-%{version}-py*.egg-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc Doc/build/html/{_static,designspaceLib,misc,pens,ttLib,varLib,*.html,*.js}
%endif
