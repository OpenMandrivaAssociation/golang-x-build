# Bootstrap needed to avoid circular dep with github.com/shurcooL
%bcond_with bootstrap
# Run tests in check section
# disable for bootstrapping
%bcond_without check

%global goipath         golang.org/x/build
%global forgeurl        https://github.com/golang/build
%global commit          57258c564e6f790b19d257469cced6b6ab47f38c

%global common_description %{expand:
Packages and tools that support Go's build system and the development 
of the Go programming language.}

%gometa

Name:           %{goname}
Version:        0
Release:        0.4%{?dist}
Summary:        Continuous build and release infrastructure 
License:        BSD
URL:            %{gourl}
Source0:        %{gosource}


BuildRequires: golang(github.com/bradfitz/go-smtpd/smtpd)
BuildRequires: golang(github.com/jellevandenhooff/dkim)
BuildRequires: golang(github.com/golang/protobuf/proto)
BuildRequires: golang(github.com/golang/protobuf/ptypes)
BuildRequires: golang(github.com/golang/protobuf/ptypes/timestamp)
BuildRequires: golang(github.com/google/go-github/github)
BuildRequires: golang(github.com/gregjones/httpcache)
BuildRequires: golang(github.com/tarm/serial)
%if %{without bootstrap}
BuildRequires: golang(github.com/shurcooL/gofontwoff)
BuildRequires: golang(github.com/shurcooL/httpgzip)
BuildRequires: golang(github.com/shurcooL/issues)
BuildRequires: golang(github.com/shurcooL/issues/maintner)
BuildRequires: golang(github.com/shurcooL/issuesapp)
%endif
BuildRequires: golang(golang.org/x/crypto/acme/autocert)
BuildRequires: golang(golang.org/x/net/context/ctxhttp)
BuildRequires: golang(golang.org/x/net/http2)
BuildRequires: golang(golang.org/x/oauth2)
BuildRequires: golang(golang.org/x/oauth2/google)
BuildRequires: golang(golang.org/x/sync/errgroup)
BuildRequires: golang(google.golang.org/api/compute/v1)
BuildRequires: golang(google.golang.org/api/container/v1)
BuildRequires: golang(google.golang.org/api/googleapi)
BuildRequires: golang(google.golang.org/api/iterator)
BuildRequires: golang(google.golang.org/appengine)
BuildRequires: golang(google.golang.org/appengine/datastore)
BuildRequires: golang(google.golang.org/appengine/delay)
BuildRequires: golang(google.golang.org/appengine/log)
BuildRequires: golang(google.golang.org/appengine/memcache)
BuildRequires: golang(google.golang.org/appengine/urlfetch)
BuildRequires: golang(google.golang.org/genproto/googleapis/api/label)
BuildRequires: golang(google.golang.org/genproto/googleapis/api/metric)
BuildRequires: golang(google.golang.org/genproto/googleapis/monitoring/v3)
BuildRequires: golang(gopkg.in/inf.v0)

%if %{with check}
BuildRequires: golang(github.com/davecgh/go-spew/spew)
BuildRequires: golang(github.com/google/go-cmp/cmp)
BuildRequires: golang(golang.org/x/net/nettest)
%endif

%description
%{common_description}


%package devel
Summary:       %{summary}

%description devel
%{common_description}

This package contains library source intended for
building other packages which use import path with
%{goipath} prefix.


%prep
%forgeautosetup

rm -rf vendor
%if %{with bootstrap}
rm -rf maintner/cmd/maintserve
%endif


%if %{without bootstrap}
%build 
%gobuildroot
for cmd in $(ls -1 cmd) ; do
   %gobuild -o _bin/$cmd %{goipath}/cmd/$cmd
done
%gobuild -o _bin/$cmd %{goipath}/maintner/cmd/maintserve
%endif


%install
%goinstall
%if %{without bootstrap}
for cmd in $(ls -1 _bin) ; do
  install -Dpm 0755 _bin/$cmd %{buildroot}%{_bindir}/$cmd
done
%endif


%if %{with check}
%check
%gochecks -d "maintner/godata" -t "maintner/maintnerd"
%endif


%if %{without bootstrap}
%files
%license LICENSE PATENTS
%{_bindir}/*
%endif


%files devel -f devel.file-list
%license LICENSE PATENTS
%doc README.md CONTRIBUTORS CONTRIBUTING.md AUTHORS


%changelog
* Fri Oct 26 2018 Robert-André Mauchin <zebob.m@gmail.com> - 0-0.5-20181026git57258c5
- Bump to commit 57258c564e6f790b19d257469cced6b6ab47f38c

* Thu Jul 19 2018 Robert-André Mauchin <zebob.m@gmail.com> - 0-0.4-20180719git0d6a646
- Bump to commit 0d6a6460c5f4e4635dc491e7226fc7cc133f9c34

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0-0.3.git0da8e46
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Mar 21 2018 Robert-André Mauchin <zebob.m@gmail.com> - 0-0.2-20180509git0da8e46
- Unboostrap

* Wed Mar 21 2018 Robert-André Mauchin <zebob.m@gmail.com> - 0-0.1-20180421git86f50f0
- First package for Fedora

