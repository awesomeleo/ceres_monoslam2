Name:           ceres-solver
Version:        1.5.0
# Release candidate versions are messy. Give them a release of
# e.g. "0.1.0%{?dist}" for RC1 (and remember to adjust the Source0
# URL). Non-RC releases go back to incrementing integers starting at 1.
Release:        0.1.0%{?dist}
Summary:        A non-linear least squares minimizer

Group:          Development/Libraries
License:        BSD
URL:            http://code.google.com/p/ceres-solver/
Source0:        http://%{name}.googlecode.com/files/%{name}-%{version}rc1.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%if (0%{?rhel} == 06)
BuildRequires:  cmake28
%else
BuildRequires:  cmake
%endif
BuildRequires:  eigen3-devel
BuildRequires:  suitesparse-devel
# Use atlas for BLAS and LAPACK
BuildRequires:  atlas-devel
BuildRequires:  protobuf-devel
BuildRequires:  gflags-devel
BuildRequires:  glog-devel

%description
Ceres Solver is a portable C++ library that allows for modeling and solving
large complicated nonlinear least squares problems. Features include:

  - A friendly API: build your objective function one term at a time
  - Automatic differentiation
  - Robust loss functions
  - Local parameterizations
  - Threaded Jacobian evaluators and linear solvers
  - Levenberg-Marquardt and Dogleg (Powell & Subspace) solvers
  - Dense QR and Cholesky factorization (using Eigen) for small problems
  - Sparse Cholesky factorization (using SuiteSparse) for large sparse problems
  - Specialized solvers for bundle adjustment problems in computer vision
  - Iterative linear solvers for general sparse and bundle adjustment problems
  - Runs on Linux, Windows, Mac OS X and Android. An iOS port is underway

Notable use of Ceres Solver is for the image alignment in Google Maps and for
vehicle pose in Google Street View.


%package        devel
Summary:        A non-linear least squares minimizer
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q

%build
mkdir build
pushd build

# Disable the compilation flags that rpmbuild macros try to apply to all
# packages because it breaks the build since release 1.5.0rc1
%define optflags ""
%if (0%{?rhel} == 06)
%{cmake28} .. \
%else
%{cmake} .. \
%endif
    -DBLAS_LIB:FILEPATH=%{_libdir}/atlas/libatlas.so \
    -DLAPACK_LIB:FILEPATH=%{_libdir}/atlas/liblapack.so
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
pushd build
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name '*.la' -delete


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%doc
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/*.a


%changelog
* Sun Feb 24 2013 Taylor Braun-Jones <taylor@braun-jones.org> - 1.5.0-0.1.0
- Bump version.

* Sun Oct 14 2012 Taylor Braun-Jones <taylor@braun-jones.org> - 1.4.0-0
- Initial creation
