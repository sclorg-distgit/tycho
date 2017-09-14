%global pkg_name tycho
%{?scl:%scl_package %{pkg_name}}
# Bootstrap build
# Tycho depends on itself, and Eclipse to build but in certain cases
# these requirements may not be satisfiable.

# Set 'tycho_bootstrap' if Tycho from buildroot is broken or non-existent
# This basically uses javac + xmvn to build only the Tycho components
# required to perform a full Tycho build
# Most common usage : A library (in Fedora) used by Tycho's runtime broke API
%global tycho_bootstrap 0
# Set 'eclipse_bootstrap' if Eclipse from buildroot cannot help build Tycho
# This basically provides a location for usage of pre-bundled Eclipse
# Possible uses : Need to build Tycho before Eclipse in fresh buildroot
%global eclipse_bootstrap 0
# When building version under development (non-release)
# %%global snap -SNAPSHOT
%global snap %{nil}

%global git_tag tycho-0.23.0

%global fp_p2_sha 09403d
%global fp_p2_version 0.0.1
%global fp_p2_snap -SNAPSHOT

%define __requires_exclude osgi*
%{?java_common_find_provides_and_requires}

Name:           %{?scl_prefix}tycho
Version:        0.23.0
Release:        8.2%{?dist}
Summary:        Plugins and extensions for building Eclipse plugins and OSGI bundles with Maven

# license file is missing but all files having some licensing information are ASL 2.0
License:        ASL 2.0 and EPL
URL:            http://eclipse.org/tycho
Source0:        http://git.eclipse.org/c/tycho/org.eclipse.tycho.git/snapshot/org.eclipse.tycho-%{git_tag}.tar.xz

# this is a workaround for maven-plugin-plugin changes that happened after
# version 2.4.3 (impossible to have empty mojo created as aggregate). This
# should be fixed upstream properly
Source1:        EmptyMojo.java
Source2:        %{pkg_name}-scripts.sh
Source3:        %{pkg_name}-bootstrap.sh
Source4:        %{pkg_name}-debundle.sh
# Fedora Eclipse bundles (needed when Eclipse not present) to build Tycho
%if %{eclipse_bootstrap}
Source5:        eclipse-bootstrap.tar.xz
%endif
# Eclipse Plugin Project supporting filesystem as p2 repository
# https://github.com/rgrunber/fedoraproject-p2
# Generated using 'git archive --prefix=fedoraproject-p2/ -o fedoraproject-p2-%%{fp_p2_sha}.tar %%{fp_p2_sha} && xz fedoraproject-p2-%%{fp_p2_sha}.tar'
Source6:        fedoraproject-p2-%{fp_p2_sha}.tar.xz
# Script that can be used to install or simulate installation of P2
# artifacts. It is used in OSGi requires generation.
Source7:        p2-install.sh

Patch0:         %{pkg_name}-fix-build.patch
Patch1:         %{pkg_name}-port-to-maven-3.0.5.patch
Patch2:         %{pkg_name}-fix-surefire.patch
Patch3:         %{pkg_name}-use-custom-resolver.patch
Patch4:         %{pkg_name}-maven-delegation.patch
# Additional changes needed just for bootstrap build
Patch5:         %{pkg_name}-fix-bootstrap-build.patch
Patch6:         %{pkg_name}-port-to-jetty-9.3.0.patch
Patch7:         %{pkg_name}-java-7-compatibility.patch
Patch8:         %{pkg_name}-port-to-xmvn-2.1.0.patch

BuildArch:      noarch

#BuildRequires:  java-devel >= 1:1.8
BuildRequires:  %{?scl_prefix_java_common}maven-local >= 4.2.0
BuildRequires:  %{?scl_prefix_maven}maven-clean-plugin
BuildRequires:  %{?scl_prefix_maven}maven-dependency-plugin
BuildRequires:  %{?scl_prefix_maven}maven-install-plugin
BuildRequires:  %{?scl_prefix_maven}maven-release-plugin
BuildRequires:  %{?scl_prefix_maven}maven-verifier
BuildRequires:  %{?scl_prefix_java_common}objectweb-asm5
BuildRequires:  %{?scl_prefix_maven}plexus-containers-component-metadata
BuildRequires:  %{?scl_prefix_maven}apache-commons-exec
BuildRequires:  %{?scl_prefix_java_common}bcel
BuildRequires:  %{?scl_prefix}decentxml
BuildRequires:  %{?scl_prefix_java_common}easymock3
BuildRequires:  %{?scl_prefix_java_common}ecj >= 4.4.2
BuildRequires:  %{?scl_prefix_maven}maven-plugin-testing-harness
BuildRequires:  %{?scl_prefix_maven}xmvn-parent-pom
%if %{tycho_bootstrap}
BuildRequires:  %{?scl_prefix_maven}maven-deploy-plugin
BuildRequires:  %{?scl_prefix_maven}maven-site-plugin
%else
BuildRequires:  %{name}
%endif
%if %{eclipse_bootstrap}
# Dependencies for Eclipse bundles we use
BuildRequires:  %{?scl_prefix}eclipse-filesystem
BuildRequires:  %{?scl_prefix_java_common}apache-commons-jxpath
BuildRequires:  %{?scl_prefix_java_common}geronimo-annotation
BuildRequires:  %{?scl_prefix_java_common}glassfish-jsp-api
BuildRequires:  %{?scl_prefix}icu4j
BuildRequires:  %{?scl_prefix_maven}sac
BuildRequires:  %{?scl_prefix}sat4j
BuildRequires:  %{?scl_prefix_java_common}xz-java
%else
BuildRequires:  %{?scl_prefix}eclipse-platform
%endif
BuildRequires:  %{?scl_prefix_java_common}jetty-http
BuildRequires:  %{?scl_prefix_java_common}jetty-util
BuildRequires:  %{?scl_prefix_java_common}jetty-security
BuildRequires:  %{?scl_prefix_java_common}jetty-server
BuildRequires:  %{?scl_prefix_java_common}jetty-servlet
BuildRequires:  %{?scl_prefix_maven}maven-shared-utils
BuildRequires:  %{?scl_prefix}mockito
BuildRequires:  zip

Requires:       %{?scl_prefix_maven}apache-commons-exec
Requires:       %{?scl_prefix}decentxml
Requires:       %{?scl_prefix_java_common}maven-local >= 4.2.0
Requires:       %{?scl_prefix_maven}maven-dependency-plugin
Requires:       %{?scl_prefix_maven}maven-verifier
Requires:       %{?scl_prefix_java_common}objectweb-asm5
Requires:       %{?scl_prefix_java_common}ecj >= 4.4.2
%if ! %{eclipse_bootstrap}
Requires:       %{?scl_prefix}eclipse-platform
%endif

# Tycho always tries to resolve all build plugins, even if they are
# not needed during Maven lifecycle.  This means that Tycho will try
# to resolve plugins like clean, deploy or site, which aren't normally
# used during package build.  See rhbz#971301
Requires:       %{?scl_prefix_maven}maven-clean-plugin
Requires:       %{?scl_prefix_maven}maven-deploy-plugin
Requires:       %{?scl_prefix_maven}maven-install-plugin
Requires:       %{?scl_prefix_maven}maven-site-plugin

%description
Tycho is a set of Maven plugins and extensions for building Eclipse
plugins and OSGI bundles with Maven. Eclipse plugins and OSGI bundles
have their own metadata for expressing dependencies, source folder
locations, etc. that are normally found in a Maven POM. Tycho uses
native metadata for Eclipse plugins and OSGi bundles and uses the POM
to configure and drive the build. Tycho supports bundles, fragments,
features, update site projects and RCP applications. Tycho also knows
how to run JUnit test plugins using OSGi runtime and there is also
support for sharing build results using Maven artifact repositories.

Tycho plugins introduce new packaging types and the corresponding
lifecycle bindings that allow Maven to use OSGi and Eclipse metadata
during a Maven build. OSGi rules are used to resolve project
dependencies and package visibility restrictions are honored by the
OSGi-aware JDT-based compiler plugin. Tycho will use OSGi metadata and
OSGi rules to calculate project dependencies dynamically and injects
them into the Maven project model at build time. Tycho supports all
attributes supported by the Eclipse OSGi resolver (Require-Bundle,
Import-Package, Eclipse-GenericRequire, etc). Tycho will use proper
classpath access rules during compilation. Tycho supports all project
types supported by PDE and will use PDE/JDT project metadata where
possible. One important design goal in Tycho is to make sure there is
no duplication of metadata between POM and OSGi metadata.



%package javadoc
Summary:        Javadocs for %{pkg_name}

%description javadoc
This package contains the API documentation for %{pkg_name}.

%prep
%setup -q -n org.eclipse.tycho-%{git_tag}

# Prepare fedoraproject-p2
tar -xf %{SOURCE6}

%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
%pom_disable_module org.fedoraproject.p2.tests fedoraproject-p2

%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch6 -p0
%patch7 -p1
%patch8 -p1

find tycho-core -iname '*html' -delete

sed -i -e 's/org.apache.maven.it.util.DirectoryScanner/org.apache.maven.shared.utils.io.DirectoryScanner/g' tycho-testing-harness/src/main/java/org/eclipse/tycho/test/AbstractTychoIntegrationTest.java

# place empty mojo in place
mkdir -p tycho-maven-plugin/src/main/java/org/fedoraproject
pushd tycho-maven-plugin/src/main/java/org/fedoraproject
cp %{SOURCE1} .
popd

# These units cannot be found during a regular build
sed -i '/^<unit id=.*$/d' tycho-bundles/tycho-bundles-target/tycho-bundles-target.target

# We do not ship org.eclipse.jdt.compiler.apt
%pom_remove_dep "org.eclipse.tycho:org.eclipse.jdt.compiler.apt"
%pom_remove_dep "org.eclipse.tycho:org.eclipse.jdt.compiler.apt" tycho-compiler-jdt

# org.ow2.asm:asm-debug-all -> org.ow2.asm:asm-all
%pom_xpath_set "pom:dependency[pom:artifactId='asm-debug-all']/pom:artifactId" "asm-all" tycho-artifactcomparator

# we don't have org.apache.commons:commons-compress:jar:sources
%pom_xpath_remove "pom:dependency[pom:classifier='sources' and pom:artifactId='commons-compress']" tycho-p2/tycho-p2-director-plugin

# Previously, JUnit would re-export Hamcrest
# Now modules using org.hamcrest.core must state the requirement explicitly
for mod in tycho-bundles/org.eclipse.tycho.{p2.{maven.repository.tests,resolver.impl.test,tools.tests},test.utils,core.shared.tests}; do
  sed -i 's/^Require-Bundle://
          /org\.junit/ i Require-Bundle: org.hamcrest.core,' \
          $mod/META-INF/MANIFEST.MF
done

# Fix bundle names
sed -i -e 's/org\.hamcrest/org.hamcrest.core/' tycho-bundles/pom.xml
sed -i -e 's/org\.mockito/org.mockito.mockito-core/' tycho-bundles/org.eclipse.tycho.p2.tools.tests/META-INF/MANIFEST.MF

# Bootstrap Build
%if %{eclipse_bootstrap}
tar -xf %{SOURCE5}
%endif

%if %{tycho_bootstrap}

%patch5 -p1

# Perform the 'minimal' (bootstrap) build of Tycho
cp %{SOURCE2} %{SOURCE3} .
./%{pkg_name}-bootstrap.sh %{eclipse_bootstrap}

%patch5 -p1 -R

# Non-Bootstrap Build
%else

# Set some temporary build version so that the bootstrapped build has
# a different version from the nonbootstrapped. Otherwise there will
# be cyclic dependencies.

medadataFile=%{_datadir}/maven-metadata/tycho.xml
sysVer=`grep -C 1 "<artifactId>tycho</artifactId>" %{_mavenpomdir}/JPP.tycho-main.pom | grep "version" | sed 's/.*>\(.*\)<.*/\1/'`
mkdir boot

# Copy Tycho POMs from system repo and set their versions to %%{version}-SNAPSHOT.
for pom in $(grep 'pom</ns[0-9]:path>' $medadataFile | sed 's|.*>\(.*\)<.*|\1|'); do
    sed '
    s/$sysVer/%{version}-SNAPSHOT/g
    s/%{fp_p2_version}%{fp_p2_snap}/%{fp_p2_version}/
' <$pom >boot/$(basename $pom)
done

# Update Maven lifecycle mappings for Tycho packaging types provided by tycho-maven-plugin.
cp %{_javadir}/tycho/tycho-maven-plugin.jar boot/tycho-maven-plugin.jar
jar xf boot/tycho-maven-plugin.jar META-INF/plexus/components.xml
sed -i s/$sysVer/%{version}-SNAPSHOT/ META-INF/plexus/components.xml
jar uf boot/tycho-maven-plugin.jar META-INF/plexus/components.xml

# Create XMvn metadata for the new JARs and POMs by customizing system Tycho metadata.
sed '
  s|>/[^<]*/\([^/]*\.pom\)</\(ns[0-9]\):path>|>'$PWD'/boot/\1</\2:path>|
  s|>'$sysVer'</\(ns[0-9]\):version>|>%{version}-SNAPSHOT</\1:version><\1:compatVersions><\1:version>%{version}-SNAPSHOT</\1:version></\1:compatVersions>|
  s|>'%{fp_p2_version}%{fp_p2_snap}'</\(ns[0-9]\):version>|>%{fp_p2_version}</\1:version><\1:compatVersions><\1:version>%{fp_p2_version}</\1:version></\1:compatVersions>|
  s|%{_javadir}/tycho/tycho-maven-plugin.jar|'$PWD'/boot/tycho-maven-plugin.jar|
' $medadataFile >boot/tycho-metadata.xml
%mvn_config resolverSettings/metadataRepositories/repository $PWD/boot/tycho-metadata.xml

%endif

# Tests are skipped anyways, so remove some test dependencies
%pom_xpath_remove "pom:dependency[pom:classifier='tests']" tycho-compiler-plugin
%pom_xpath_remove "pom:dependency[pom:classifier='tests']" tycho-packaging-plugin

%{?scl:EOF}

%build
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
xmvn -o -Dtycho-version=%{version}-SNAPSHOT -Dmaven.test.skip=true \
-Dmaven.repo.local=$(pwd)/.m2 -Dfedora.p2.repos=$(pwd)/bootstrap \
-f fedoraproject-p2/pom.xml \
clean install org.apache.maven.plugins:maven-javadoc-plugin:aggregate

xmvn -o -DtychoBootstrapVersion=%{version}-SNAPSHOT -Dmaven.test.skip=true \
-Dmaven.repo.local=$(pwd)/.m2 -Dfedora.p2.repos=$(pwd)/bootstrap \
clean install org.apache.maven.plugins:maven-javadoc-plugin:aggregate
%{?scl:EOF}

%install
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}

cp %{SOURCE2} %{SOURCE4} .

install -dm 755 $RPM_BUILD_ROOT%{_javadir}/tycho
install -dm 755 $RPM_BUILD_ROOT%{_mavenpomdir}

# fedoraproject-p2 parent
mod=fedoraproject-p2
install -pm 644 $mod/pom.xml $RPM_BUILD_ROOT%{_mavenpomdir}/JPP.%{pkg_name}-$mod.pom
%add_maven_depmap JPP.%{pkg_name}-$mod.pom

# fedoraproject-p2
for mod in fedoraproject-p2/{org.fedoraproject.p2,xmvn-p2-installer-plugin}; do
   echo $mod
   aid=`basename $mod`
   install -pm 644 $mod/pom.xml  $RPM_BUILD_ROOT%{_mavenpomdir}/JPP.%{pkg_name}-$aid.pom
   install -m 644 $mod/target/$aid-%{fp_p2_version}%{fp_p2_snap}.jar $RPM_BUILD_ROOT%{_javadir}/%{pkg_name}/$aid.jar
   %add_maven_depmap JPP.%{pkg_name}-$aid.pom %{pkg_name}/$aid.jar -a "org.eclipse.tycho:$aid"
done

# pom and jar installation
for mod in target-platform-configuration tycho-compiler-{jdt,plugin} \
           tycho-{artifactcomparator,core,embedder-api,metadata-model,testing-harness} \
           sisu-equinox/sisu-equinox{-api,-launching,-embedder} \
           tycho-p2/tycho-p2-{facade,plugin,{director,publisher,repository}-plugin} \
           tycho-{maven,packaging,pomgenerator,release/tycho-versions,source}-plugin \
           tycho-bundles/org* \
           tycho-surefire/{tycho-surefire-plugin,org.eclipse.tycho.surefire.{osgibooter,junit,junit4{,7}}}; do
   echo $mod
   aid=`basename $mod`
   install -pm 644 $mod/pom.xml  $RPM_BUILD_ROOT%{_mavenpomdir}/JPP.%{pkg_name}-$aid.pom
   install -m 644 $mod/target/$aid-%{version}%{snap}.jar $RPM_BUILD_ROOT%{_javadir}/%{pkg_name}/$aid.jar
   %add_maven_depmap JPP.%{pkg_name}-$aid.pom %{pkg_name}/$aid.jar -a "org.eclipse.tycho:$aid"
done

# pom installation
for pommod in tycho-p2 tycho-bundles tycho-surefire \
              tycho-release sisu-equinox; do
   aid=`basename $pommod`
   install -pm 644 $pommod/pom.xml \
               $RPM_BUILD_ROOT%{_mavenpomdir}/JPP.%{pkg_name}-$aid.pom
   %add_maven_depmap JPP.%{pkg_name}-$aid.pom -a "org.eclipse.tycho:$aid"
done

# p2 runtime
dir=.m2/org/eclipse/tycho/tycho-bundles-external/%{version}%{snap}
%if ! %{eclipse_bootstrap}
./%{pkg_name}-debundle.sh tycho-bundles/tycho-bundles-external/ $dir/tycho-bundles-external-%{version}*.zip $RPM_BUILD_ROOT%{_javadir}/%{pkg_name}/tycho-bundles-external-manifest.txt
%endif
install -pm 644 $dir/tycho-bundles-external-%{version}*.pom $RPM_BUILD_ROOT%{_mavenpomdir}/JPP.%{pkg_name}-tycho-bundles-external.pom
install -m 644 $dir/tycho-bundles-external-%{version}*.zip $RPM_BUILD_ROOT%{_javadir}/%{pkg_name}/tycho-bundles-external.zip
%add_maven_depmap JPP.%{pkg_name}-tycho-bundles-external.pom %{pkg_name}/tycho-bundles-external.zip -a "org.eclipse.tycho:tycho-bundles-external"
%if ! %{eclipse_bootstrap}
%add_maven_depmap org.eclipse.tycho:tycho-bundles-external:txt:manifest:%{version}%{snap} %{pkg_name}/tycho-bundles-external-manifest.txt
%endif

# main
install -pm 644 pom.xml  $RPM_BUILD_ROOT%{_mavenpomdir}/JPP.%{pkg_name}-main.pom
%add_maven_depmap JPP.%{pkg_name}-main.pom

# standalone p2 director
%if ! %{eclipse_bootstrap}
./%{pkg_name}-debundle.sh tycho-bundles/tycho-standalone-p2-director/ .m2/org/eclipse/tycho/tycho-standalone-p2-director/%{version}%{snap}/tycho-standalone-p2-director-%{version}*.zip
%endif
pushd .m2/org/eclipse/tycho/tycho-standalone-p2-director/%{version}%{snap}/
install -m 644 tycho-standalone-p2-director-%{version}*.zip $RPM_BUILD_ROOT%{_javadir}/%{pkg_name}/tycho-standalone-p2-director.zip
install -pm 644 tycho-standalone-p2-director-%{version}*.pom $RPM_BUILD_ROOT%{_mavenpomdir}/JPP.%{pkg_name}-tycho-standalone-p2-director.pom
popd
%add_maven_depmap JPP.%{pkg_name}-tycho-standalone-p2-director.pom tycho/tycho-standalone-p2-director.zip -a "org.eclipse.tycho:tycho-standalone-p2-director"

# javadoc
install -dm 755 $RPM_BUILD_ROOT%{_javadocdir}/tycho
cp -pr target/site/api*/* $RPM_BUILD_ROOT%{_javadocdir}/tycho

# p2-install script
install -dm 755 $RPM_BUILD_ROOT%{_javadir}-utils/
install -pm 755 %{SOURCE7} $RPM_BUILD_ROOT%{_javadir}-utils/

%if %{eclipse_bootstrap}
# org.eclipse.osgi
osgiJarPath=`find ".m2/org" -name "org.eclipse.osgi_*.jar"`

# http://git.eclipse.org/c/linuxtools/org.eclipse.linuxtools.eclipse-build.git/tree/externalpoms/org.eclipse.osgi.pom
echo '<?xml version="1.0" encoding="UTF-8"?>
<project xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/maven-v4_0_0.xsd" xsi:noNamespaceSchemaLocation="http://maven.apache.org/POM/4.0.0">
  <modelVersion>4.0.0</modelVersion>
  <groupId>org.eclipse.osgi</groupId>
  <artifactId>org.eclipse.osgi</artifactId>
  <version>3.10.100.v20150602-1500</version>
</project>' > JPP.tycho-osgi.pom

install -pm 644 JPP.tycho-osgi.pom $RPM_BUILD_ROOT%{_mavenpomdir}/JPP.tycho-osgi.pom
install -m 644 $osgiJarPath $RPM_BUILD_ROOT%{_javadir}/tycho/osgi.jar
%add_maven_depmap JPP.tycho-osgi.pom tycho/osgi.jar -a "org.eclipse.tycho:org.eclipse.osgi"

# org.eclipse.osgi.compatibility.state
osgiStateJarPath=`find ".m2/org" -name "org.eclipse.osgi.compatibility.state_*.jar"`

# http://git.eclipse.org/c/linuxtools/org.eclipse.linuxtools.eclipse-build.git/tree/externalpoms/org.eclipse.osgi.compatibility.state.pom
echo '<?xml version="1.0" encoding="UTF-8"?>
<project xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/maven-v4_0_0.xsd" xsi:noNamespaceSchemaLocation="http://maven.apache.org/POM/4.0.0">
  <modelVersion>4.0.0</modelVersion>
  <groupId>org.eclipse.osgi</groupId>
  <artifactId>org.eclipse.osgi.compatibility.state</artifactId>
  <version>1.0.100.v20150602-1500</version>
</project>' > JPP.tycho-osgi.compatibility.state.pom

install -pm 644 JPP.tycho-osgi.compatibility.state.pom $RPM_BUILD_ROOT%{_mavenpomdir}/JPP.tycho-osgi.compatibility.state.pom
install -m 644 $osgiStateJarPath $RPM_BUILD_ROOT%{_javadir}/tycho/osgi.compatibility.state.jar
%add_maven_depmap JPP.tycho-osgi.compatibility.state.pom tycho/osgi.compatibility.state.jar -a "org.eclipse.tycho:org.eclipse.osgi.compatibility.state"
%endif

# Symlink XMvn P2 plugin with all dependencies so that it can be loaded by XMvn
install -dm 755 %{buildroot}%{?_scl_prefix}%{?scl_maven:/%{scl_maven}/root}%{_root_datadir}/xmvn/lib/installer/
%if %{eclipse_bootstrap}
ln -s %{_javadir}/tycho/osgi.jar %{buildroot}%{?_scl_prefix}%{?scl_maven:/%{scl_maven}/root}%{_root_datadir}/xmvn/lib/installer/
%else
ln -s %{_javadir}/eclipse/osgi.jar %{buildroot}%{?_scl_prefix}%{?scl_maven:/%{scl_maven}/root}%{_root_datadir}/xmvn/lib/installer/
%endif
ln -s %{_javadir}/tycho/xmvn-p2-installer-plugin.jar %{buildroot}%{?_scl_prefix}%{?scl_maven:/%{scl_maven}/root}%{_root_datadir}/xmvn/lib/installer/
ln -s %{_javadir}/tycho/org.fedoraproject.p2.jar %{buildroot}%{?_scl_prefix}%{?scl_maven:/%{scl_maven}/root}%{_root_datadir}/xmvn/lib/installer/
%{?scl:EOF}

%files -f .mfiles
%dir %{_javadir}/tycho
%{?_scl_prefix}%{?scl_maven:/%{scl_maven}/root}%{_root_datadir}/xmvn/lib/installer/*
%{_javadir}-utils/p2-install.sh
%doc README.md

%files javadoc
%{_javadocdir}/tycho

%changelog
* Tue Aug 04 2015 Mat Booth <mat.booth@redhat.com> - 0.23.0-8.2
- Tighten up the dependency on ecj, rhbz#1249293

* Tue Jul 28 2015 Roland Grunberg <rgrunber@redhat.com> - 0.23.0-8.1
- fedoraproject-p2: Single IU resolving requirements with multiple matches.

* Mon Jul 06 2015 Mat Booth <mat.booth@redhat.com> - 0.23.0-5.4
- Non-bootstrap build

* Tue Jun 30 2015 Mat Booth <mat.booth@redhat.com> - 0.23.0-5.3
- fedoraproject-p2: Allow xmvn-p2-installer to work in bootstrap mode

* Mon Jun 29 2015 Roland Grunberg <rgrunber@redhat.com> - 0.23.0-5.2
- Support extraction of symlinks with plexus-archiver < 2.4.4-4.
- Re-enable o.e.tycho.p2.{maven.repository,tools}.tests.
- Add BuildRequires on zip.

* Sun Jun 28 2015 Roland Grunberg <rgrunber@redhat.com> - 0.23.0-5.1
- Additional fixes for SCL-iziation.
- Port to maven-surefire 2.15
- Port to plexus-archiver 2.4
- Disable usesNativeCode due to issue with objectweb-asm.
- Disable o.e.tycho.p2.{maven.repository,tools}.tests due to mockito.

* Fri Jun 26 2015 Roland Grunberg <rgrunber@redhat.com> - 0.23.0-5.1
- SCL-ize.
- Make bootstrap build work with maven-plugin-plugin < 3.2
- Port to work with Maven 3.0.5
- Port to work with Java 7
- Port to work with XMvn 2.1.0

* Fri Jun 26 2015 Roland Grunberg <rgrunber@redhat.com> - 0.23.0-5.1
- Initial import of tycho-0.23.0-5.fc23.
