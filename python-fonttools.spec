#
# Conditional build:
%bcond_without	python2	# CPython 2.x module
%bcond_with	python3	# CPython 3.x module (version 4+ built from fonttools.spec)
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# pytest tests

Summary:	Python 2 tools to manipulate font files
Summary(pl.UTF-8):	Narzędzia do manipulacji na plikach fontów dla Pythona 2
Name:		python-fonttools
Version:	3.44.0
Release:	8
# basic license is BSD
# FontTools includes Adobe AGL & AGLFN, which is under 3-clauses BSD license
License:	MIT, BSD
Group:		Development/Tools
#Source0Download: https://github.com/fonttools/fonttools/releases
Source0:	https://github.com/fonttools/fonttools/archive/%{version}/fonttools-%{version}.tar.gz
# Source0-md5:	3f9ff311081a0f591a09552902671d29
Patch0:		%{name}-singledispatch.patch
URL:		https://github.com/fonttools/fonttools
%if %(locale -a | grep -q '^C\.utf8$'; echo $?)
BuildRequires:	glibc-localedb-all
%endif
%if %{with python2}
BuildRequires:	python-devel >= 1:2.7
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-brotli
BuildRequires:	python-enum34 >= 1.1.6
BuildRequires:	python-fs >= 2.2.0
BuildRequires:	python-pytest >= 3.0
BuildRequires:	python-unicodedata2 >= 12.0.0
%endif
%endif
%if %{with python3}
BuildRequires:	python3-devel >= 1:3.4
%if %{with tests}
BuildRequires:	pythoni3-brotli
BuildRequires:	python3-fs >= 2.2.0
BuildRequires:	python3-pytest >= 3.0
%if "%{ver_lt '%{py3_ver}' '3.7'}" == "1"
BuildRequires:	python3-unicodedata2 >= 12.0.0
%endif
%endif
%endif
BuildRequires:	rpmbuild(macros) >= 1.750
%if %{with doc}
BuildRequires:	sphinx-pdg-2 >= 1.5.5
%endif
Requires:	python-modules >= 1:2.7
Requires:	python-unicodedata2 >= 12.0.0
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Python 2 tools to manipulate font files.

%description -l pl.UTF-8
Narzędzia do manipulacji na plikach fontów dla Pythona 2.

%package apidocs
Summary:	Documentation for Python fonttools module
Summary(pl.UTF-8):	Dokumentacja modułu Pythona fonttools
Group:		Documentation

%description apidocs
Documentation for Python fonttools module.

%description apidocs -l pl.UTF-8
Dokumentacja modułu Pythona fonttools.

%package -n python3-fonttools
Summary:	Python 3 tools to manipulate font files
Summary(pl.UTF-8):	Narzędzia do manipulacji na plikach fontów dla Pythona 3
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.4
%if "%{ver_lt '%{py3_ver}' '3.7'}" == "1"
Requires:	python3-unicodedata2 >= 12.0.0
%endif

%description -n python3-fonttools
Python 3 tools to manipulate font files.

%description -n python3-fonttools -l pl.UTF-8
Narzędzia do manipulacji na plikach fontów dla Pythona 3.

%prep
%setup -q -n fonttools-%{version}
%patch -P 0 -p1

%build
export LC_ALL=C.UTF-8
%if %{with python2}
%py_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTHONPATH=Lib \
%{__python} -m pytest Tests
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTHONPATH=Lib \
%{__python} -m pytest Tests
%endif
%endif

%if %{with doc}
PYTHONPATH=$(pwd)/build-2/lib \
%{__make} -C Doc html \
	SPHINXBUILD=sphinx-build-2
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python3}
%py3_install
%endif

%if %{with python2}
%py_install

%py_postclean
%endif

# packaged from fonttools.spec
%{__rm} -r $RPM_BUILD_ROOT{%{_bindir},%{_mandir}/man1}

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%{py_sitescriptdir}/fontTools
%{py_sitescriptdir}/fonttools-%{version}-py*.egg-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc Doc/build/html/{_static,designspaceLib,misc,pens,ttLib,varLib,*.html,*.js}
%endif
%endif

%if %{with python3}
%files -n python3-fonttools
%defattr(644,root,root,755)
%{py3_sitescriptdir}/fontTools
%{py3_sitescriptdir}/fonttools-%{version}-py*.egg-info
%endif
