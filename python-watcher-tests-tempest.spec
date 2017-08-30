%{!?upstream_version: %global upstream_version %{commit}}
%global commit 2a084eb2d599436ae3b87ecbb1ef9bd61f52776b
%global shortcommit %(c=%{commit}; echo ${c:0:7})
# DO NOT REMOVE ALPHATAG
%global alphatag .%{shortcommit}git

%global service watcher
%global plugin watcher-tempest-plugin
%global module watcher_tempest_plugin
%global with_doc 1

%if 0%{?fedora}
%global with_python3 1
%endif

%global common_desc \
This package contains Tempest tests to cover the watcher project. \
Additionally it provides a plugin to automatically load these tests into Tempest.

Name:       python-%{service}-tests-tempest
Version:    0.0.1
Release:    0.2%{?alphatag}%{?dist}
Summary:    Tempest Integration of Watcher Project
License:    ASL 2.0
URL:        https://git.openstack.org/cgit/openstack/%{plugin}/

Source0:    https://github.com/openstack/%{plugin}/archive/%{commit}.tar.gz#/%{plugin}-%{shortcommit}.tar.gz

BuildArch:  noarch

%description
%{common_desc}

%package -n python2-%{service}-tests-tempest
Summary: %{summary}
%{?python_provide:%python_provide python2-%{service}-tests-tempest}
BuildRequires:  python2-devel
BuildRequires:  python-pbr
BuildRequires:  python-setuptools
BuildRequires:  git
BuildRequires:  openstack-macros

Obsoletes:  python-watcher-tests-tempest > 1.4.1

Requires:   python-pbr
Requires:   python-six  >= 1.9.0
Requires:   python-tempest >= 1:12.2.0
Requires:   python-oslo-utils
Requires:   python-oslo-log

%description -n python2-%{service}-tests-tempest
%{common_desc}

%if 0%{?with_doc}
%package -n python-%{service}-tests-tempest-doc
Summary:        python-%{service}-tests-tempest documentation

BuildRequires:  python-sphinx
BuildRequires:  python-openstackdocstheme

%description -n python-%{service}-tests-tempest-doc
It contains the documentation for the watcher tempest plugin.
%endif

%if 0%{?with_python3}
%package -n python3-%{service}-tests-tempest
Summary: %{summary}
%{?python_provide:%python_provide python3-%{service}-tests-tempest}
BuildRequires:  python3-devel
BuildRequires:  python3-pbr
BuildRequires:  python3-setuptools

Requires:   python3-pbr
Requires:   python3-six  >= 1.9.0
Requires:   python3-tempest >= 1:12.2.0
Requires:   python3-oslo-utils
Requires:   python3-oslo-log

%description -n python3-%{service}-tests-tempest
%{common_desc}
%endif

%prep
%autosetup -n %{plugin}-%{upstream_version} -S git

# Let's handle dependencies ourseleves
%py_req_cleanup
# Remove bundled egg-ingo
rm -rf %{module}.egg-info

%build
%if 0%{?with_python3}
%py3_build
%endif
%py2_build

# Generate Docs
%if 0%{?with_doc}
%{__python2} setup.py build_sphinx -b html
# remove the sphinx build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
%if 0%{?with_python3}
%py3_install
%endif
%py2_install

%files -n python2-%{service}-tests-tempest
%license LICENSE
%doc README.rst
%{python2_sitelib}/%{module}
%{python2_sitelib}/*.egg-info

%if 0%{?with_python3}
%files -n python3-%{service}-tests-tempest
%license LICENSE
%doc README.rst
%{python3_sitelib}/%{module}
%{python3_sitelib}/*.egg-info
%endif

%if 0%{?with_doc}
%files -n python-%{service}-tests-tempest-doc
%doc doc/build/html
%license LICENSE
%endif

%changelog
* Wed Aug 30 2017 Chandan Kumar <chkumar@redhat.com> 0.0.1-0.2.2a084eb2git
- Obsoletes python-watcher-tests-tempest-1.4.1 intree plugin

* Wed Aug 30 2017 Chandan Kumar <chkumar@redhat.com> 0.0.1-0.1.2a084eb2git
- Update to pre-release 0.0.1 (2a084eb2d599436ae3b87ecbb1ef9bd61f52776b)
