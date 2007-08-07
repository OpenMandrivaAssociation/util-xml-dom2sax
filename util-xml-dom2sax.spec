%define section         free
%define gcj_support     1

Name:           util-xml-dom2sax
Version:        1.0.4
Release:        %mkrel 0.0.1
Epoch:          0
Summary:        org.freecompany.util
License:        MIT
Group:          Development/Java
URL:            http://www.freecompany.org/
# svn export https://svn.freecompany.org/public/util/tags/util-xml-dom2sax-1.0.4
# zip -9r util-xml-dom2sax-src-0.2.9.zip util-xml-dom2sax-0.2.9
Source0:        http://repository.freecompany.org/org/freecompany/util/zips/util-xml-dom2sax-src-%{version}.zip
Source1:        util-xml-dom2sax-1.0.4-build.xml
Requires:       util-multicaster
Requires:       xmlwriter
BuildRequires:  ant
BuildRequires:  ant-junit
BuildRequires:  jpackage-utils >= 0:1.6
BuildRequires:  junit
BuildRequires:  util-multicaster
BuildRequires:  xmlwriter
%if %{gcj_support}
Requires(post): java-gcj-compat
Requires(postun): java-gcj-compat
BuildRequires:  java-gcj-compat-devel
%else
BuildRequires:  java-devel
BuildArch:      noarch
%endif
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

%description
org.freecompany.util

%package javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java

%description javadoc
Javadoc for %{name}.

%prep
%setup -q
%{__cp} -a %{SOURCE1} build.xml
%{__perl} -pi -e 's|<javac|<javac nowarn="true"|g' build.xml

%build
export CLASSPATH=$(build-classpath junit util-multicaster xmlwriter)
export OPT_JAR_LIST="ant/ant-junit"
%{ant} jar javadoc test

%install
%{__rm} -rf %{buildroot}

%{__mkdir_p} %{buildroot}%{_javadir}
%{__cp} -a dist/%{name}.jar %{buildroot}%{_javadir}/%{name}-%{version}.jar
(cd %{buildroot}%{_javadir} && for jar in *-%{version}*; do %{__ln_s} ${jar} ${jar/-%{version}/}; done)

%{__mkdir_p} %{buildroot}%{_javadocdir}/%{name}-%{version}
%{__cp} -a dist/doc/* %{buildroot}%{_javadocdir}/%{name}-%{version}
%{__ln_s} %{name}-%{version} %{buildroot}%{_javadocdir}/%{name}

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%clean
%{__rm} -rf %{buildroot}

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

%files
%defattr(0644,root,root,0755)
%{_javadir}/%{name}.jar
%{_javadir}/%{name}-%{version}.jar
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/%{name}-%{version}.jar.db
%attr(-,root,root) %{_libdir}/gcj/%{name}/%{name}-%{version}.jar.so
%endif

%files javadoc
%defattr(0644,root,root,0755)
%doc %{_javadocdir}/%{name}-%{version}
%doc %{_javadocdir}/%{name}
