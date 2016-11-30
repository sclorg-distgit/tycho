%{?scl:%scl_package tycho}
%{!?scl:%global pkg_name %{name}}
%{?java_common_find_provides_and_requires}

%global baserelease 4

# Bootstrap build
# Tycho depends on itself, and Eclipse to build but in certain cases
# these requirements may not be satisfiable.

# Set 'tycho_bootstrap' if Tycho from buildroot is broken or non-existent
# This basically uses javac + xmvn to build only the Tycho components
# required to perform a full Tycho build
# Most common usage : A library (in Fedora) used by Tycho's runtime broke API
%global tycho_bootstrap 1
# Set 'eclipse_bootstrap' if Eclipse from buildroot cannot help build Tycho
# This basically provides a location for usage of pre-bundled Eclipse
# Possible uses : Need to build Tycho before Eclipse in fresh buildroot
%global eclipse_bootstrap 1
# When building version under development (non-release)
# %%global snap -SNAPSHOT
%global snap %{nil}

%global git_tag tycho-0.25.0

%global fp_p2_sha 4e1319
%global fp_p2_version 0.0.1
%global fp_p2_snap -SNAPSHOT

%define __requires_exclude osgi*

Name:           %{?scl_prefix}tycho
Version:        0.25.0
Release:        7.%{baserelease}%{?dist}
Summary:        Plugins and extensions for building Eclipse plugins and OSGI bundles with Maven

# license file is missing but all files having some licensing information are ASL 2.0
License:        ASL 2.0 and EPL
URL:            http://eclipse.org/tycho
Source0:        http://git.eclipse.org/c/tycho/org.eclipse.tycho.git/snapshot/org.eclipse.tycho-%{git_tag}.tar.xz

# this is a workaround for maven-plugin-plugin changes that happened after
# version 2.4.3 (impossible to have empty mojo created as aggregate). This
# should be fixed upstream properly
Source1:        EmptyMojo.java
Source2:        tycho-scripts.sh
Source3:        tycho-bootstrap.sh
Source4:        tycho-debundle.sh
# Fedora Eclipse bundles needed to build Tycho when Eclipse is not present
# or when the Eclipse that is present is not compatible
%if %{eclipse_bootstrap}
Source5:        eclipse-bootstrap-neon.tar.xz
%endif
# Eclipse Plugin Project supporting filesystem as p2 repository
# https://github.com/rgrunber/fedoraproject-p2
# Generated using 'git archive --prefix=fedoraproject-p2/ -o fedoraproject-p2-%%{fp_p2_sha}.tar %%{fp_p2_sha} && xz fedoraproject-p2-%%{fp_p2_sha}.tar'
Source6:        fedoraproject-p2-%{fp_p2_sha}.tar.xz
# Script that can be used to install or simulate installation of P2
# artifacts. It is used in OSGi requires generation.
Source7:        p2-install.sh

Patch0:         %{pkg_name}-fix-build.patch
Patch2:         %{pkg_name}-fix-surefire.patch
Patch3:         %{pkg_name}-use-custom-resolver.patch
Patch4:         %{pkg_name}-maven-delegation.patch
# Additional changes needed just for bootstrap build
Patch5:         %{pkg_name}-fix-bootstrap-build.patch
# Accepted upstream: https://git.eclipse.org/r/49897
#Patch7:         %{pkg_name}-port-to-plexus-archiver-3.0.1.patch
#Patch8:         tycho-maven-archiver-3.0.1.patch
Patch9:         tycho-eclipse-neon.patch
Patch10:        tycho-port-to-xmvn-2.1.0.patch
# There can be no java 8 artefacts may be in the class path when building maven
# plugins https://issues.apache.org/jira/browse/MPLUGIN-273
Patch11:        tycho-java-7-compatibility.patch

BuildArch:      noarch

BuildRequires:  %{?scl_prefix_maven}maven-local
BuildRequires:  %{?scl_prefix_maven}xmvn
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
BuildRequires:  %{?scl_prefix_java_common}easymock2
BuildRequires:  %{?scl_prefix}ecj >= 1:4.5.2-2
BuildRequires:  %{?scl_prefix_maven}maven-plugin-testing-harness
BuildRequires:  %{?scl_prefix_maven}xmvn-parent-pom
BuildRequires:  %{?scl_prefix_maven}maven-plugin-bundle
BuildRequires:  %{?scl_prefix_maven}maven-plugin-plugin
BuildRequires:  %{?scl_prefix_maven}maven-source-plugin
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
BuildRequires:  %{?scl_prefix}sac
BuildRequires:  %{?scl_prefix}sat4j
BuildRequires:  %{?scl_prefix_java_common}xz-java
%else
BuildRequires:  %{?scl_prefix}eclipse-platform >= 1:4.6.0
%endif
BuildRequires:  %{?scl_prefix_java_common}jetty-http
BuildRequires:  %{?scl_prefix_java_common}jetty-util
BuildRequires:  %{?scl_prefix_java_common}jetty-security
BuildRequires:  %{?scl_prefix_java_common}jetty-server
BuildRequires:  %{?scl_prefix_java_common}jetty-servlet
BuildRequires:  %{?scl_prefix_maven}maven-shared-utils
BuildRequires:  %{?scl_prefix}mockito
BuildRequires:  %{?scl_prefix}glassfish-servlet-api
BuildRequires:  zip

Requires:       %{?scl_prefix_maven}apache-commons-exec
Requires:       %{?scl_prefix}decentxml
Requires:       %{?scl_prefix_maven}maven-local
Requires:       %{?scl_prefix_maven}xmvn
Requires:       %{?scl_prefix_maven}maven-dependency-plugin
Requires:       %{?scl_prefix_maven}maven-verifier
Requires:       %{?scl_prefix_java_common}objectweb-asm5
Requires:       %{?scl_prefix}ecj >= 1:4.5.2-2
Requires:       %{?scl_prefix_maven}maven-plugin-testing-harness
%if ! %{eclipse_bootstrap}
Requires:       %{?scl_prefix}eclipse-platform >= 1:4.6.0
%endif

# Tycho always tries to resolve all build plugins, even if they are
# not needed during Maven lifecycle.  This means that Tycho will try
# to resolve plugins like clean, deploy or site, which aren't normally
# used during package build.  See rhbz#971301
Requires:       %{?scl_prefix_maven}maven-clean-plugin
Requires:       %{?scl_prefix_maven}maven-deploy-plugin
Requires:       %{?scl_prefix_maven}maven-install-plugin
Requires:       %{?scl_prefix_maven}maven-site-plugin

# Required by tycho-source-plugin, but XMvn fails to generate
# auto-requires due to uncommon dependency <type>maven-plugin</type>
Requires:       %{?scl_prefix_maven}maven-source-plugin

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
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
set -e -x
%setup -q -n org.eclipse.tycho-%{git_tag}

# Prepare fedoraproject-p2
tar -xf %{SOURCE6}

%pom_disable_module org.fedoraproject.p2.tests fedoraproject-p2

%patch0 -p1 -b.orig
%patch2 -p1
%patch3 -p1
%patch4 -p1
#%patch7 -p0
#%patch8 -p0
%patch9 -p0
%patch10 -p1
pushd fedoraproject-p2
%patch11 -p1
popd

find tycho-core -iname '*html' -delete

sed -i -e 's/org.apache.maven.it.util.DirectoryScanner/org.apache.maven.shared.utils.io.DirectoryScanner/g' tycho-testing-harness/src/main/java/org/eclipse/tycho/test/AbstractTychoIntegrationTest.java

# Move from org.sonatype.aether to org.eclipse.aether
find . -name "*.java" | xargs sed -i 's/org.sonatype.aether/org.eclipse.aether/g'
find . -name "*.java" | xargs sed -i 's/org.eclipse.aether.util.DefaultRepositorySystemSession/org.eclipse.aether.DefaultRepositorySystemSession/g'
sed -i 's/public int getPriority/public float getPriority/g' tycho-core/src/main/java/org/eclipse/tycho/core/p2/P2RepositoryConnectorFactory.java

# place empty mojo in place
mkdir -p tycho-maven-plugin/src/main/java/org/fedoraproject
pushd tycho-maven-plugin/src/main/java/org/fedoraproject
cp %{SOURCE1} .
popd

# These units cannot be found during a regular build
sed -i '/^<unit id=.*$/d' tycho-bundles/tycho-bundles-target/tycho-bundles-target.target

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
sed -i -e 's/org\.mockito/org.mockito.mockito-core/' \
  tycho-bundles/org.eclipse.tycho.p2.tools.tests/META-INF/MANIFEST.MF \
  tycho-bundles/org.eclipse.tycho.p2.maven.repository.tests/META-INF/MANIFEST.MF

# Bootstrap Build
%if %{eclipse_bootstrap}
# Unpack a compatible version of Eclipse we can use to build against
tar -xf %{SOURCE5}
ln -s lib64 bootstrap/usr/lib
# Install OSGi bundles into local repo to override any incompatible system version
# that may be already installed
pushd bootstrap
for f in usr/lib64/eclipse/plugins/org.eclipse.osgi.compatibility.state_*.jar \
         usr/lib64/eclipse/plugins/org.eclipse.osgi.services_*.jar \
         usr/lib64/eclipse/plugins/org.eclipse.osgi_*.jar ; do
  xmvn -o install:install-file -Dfile=$f -Dpackaging=jar -DgroupId=org.eclipse.tycho -Dmaven.repo.local=$(pwd)/../.m2 \
    -DartifactId=$(echo $(basename $f) | cut -d_ -f1) -Dversion=$(echo "${f%.jar}" | cut -d_ -f2)
done
popd
%endif

%if %{tycho_bootstrap}

%patch5 -p1

# Perform the 'minimal' (bootstrap) build of Tycho
cp %{SOURCE2} %{SOURCE3} .
./tycho-bootstrap.sh %{eclipse_bootstrap}


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

sed -i -e "s|javax.servlet|javax.servlet-api|g" tycho-bundles/org.eclipse.tycho.test.utils/META-INF/MANIFEST.MF
%{?scl:EOF}


%build
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
set -e -x
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
set -e -x
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
           tycho-bundles/org*  \
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
osgiJarPath=$(find .m2/org/eclipse/tycho/org.eclipse.osgi/*/ -name "*.jar")
osgiPomPath=$(find .m2/org/eclipse/tycho/org.eclipse.osgi/*/ -name "*.pom")

install -pm 644 $osgiPomPath $RPM_BUILD_ROOT%{_mavenpomdir}/JPP.tycho-osgi.pom
install -m 644 -T $osgiJarPath $RPM_BUILD_ROOT%{_javadir}/tycho/osgi.jar
%add_maven_depmap JPP.tycho-osgi.pom tycho/osgi.jar -a "org.eclipse.osgi:org.eclipse.osgi"

# org.eclipse.osgi.compatibility.state
osgiStateJarPath=$(find .m2/org/eclipse/tycho/org.eclipse.osgi.compatibility.state/*/ -name "*.jar")
osgiStatePomPath=$(find .m2/org/eclipse/tycho/org.eclipse.osgi.compatibility.state/*/ -name "*.pom")

install -pm 644 $osgiStatePomPath $RPM_BUILD_ROOT%{_mavenpomdir}/JPP.tycho-osgi.compatibility.state.pom
install -m 644 -T $osgiStateJarPath $RPM_BUILD_ROOT%{_javadir}/tycho/osgi.compatibility.state.jar
%add_maven_depmap JPP.tycho-osgi.compatibility.state.pom tycho/osgi.compatibility.state.jar -a "org.eclipse.osgi:org.eclipse.osgi.compatibility.state"

# org.eclipse.osgi.services
osgiServJarPath=$(find .m2/org/eclipse/tycho/org.eclipse.osgi.services/*/ -name "*.jar")
osgiServPomPath=$(find .m2/org/eclipse/tycho/org.eclipse.osgi.services/*/ -name "*.pom")

install -pm 644 $osgiServPomPath $RPM_BUILD_ROOT%{_mavenpomdir}/JPP.tycho-osgi.services.pom
install -m 644 -T $osgiServJarPath $RPM_BUILD_ROOT%{_javadir}/tycho/osgi.services.jar
%add_maven_depmap JPP.tycho-osgi.services.pom tycho/osgi.services.jar -a "org.eclipse.osgi:org.eclipse.osgi.services"

# Misc other bundles needed for bootstrapping
for bnd in \
  core.contenttype \
  core.expressions \
  core.filesystem \
  core.jobs \
  core.net \
  core.resources \
  core.runtime \
  equinox.app \
  equinox.common \
  equinox.concurrent \
  equinox.preferences \
  equinox.registry \
  equinox.security ; do
bndJarPath=$(find bootstrap -name "org.eclipse.${bnd}_*.jar")
install -m 644 -T $bndJarPath $RPM_BUILD_ROOT%{_javadir}/tycho/$bnd.jar
done
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
%{?_scl_prefix}%{?scl_maven:/%{scl_maven}/root}%{_root_datadir}/xmvn/lib/installer/*
%{_javadir}-utils/p2-install.sh
%{_javadir}/tycho/core.*.jar
%{_javadir}/tycho/equinox.*.jar
%doc README.md

%files javadoc
%{_javadocdir}/tycho

%changelog
* Wed Jul 27 2016 Mat Booth <mat.booth@redhat.com> - 0.25.0-7.4
- Work around java 8 code problems properly

* Wed Jul 27 2016 Mat Booth <mat.booth@redhat.com> - 0.25.0-7.3
- Add missing BR on zip for EL6

* Mon Jul 25 2016 Mat Booth <mat.booth@redhat.com> - 0.25.0-7.2
- Perform bootstrap build
- Drop patch for porting to plexus/maven-archiver 3.0.1
- Add patch for porting to xmvn 2.1.0
- Drop patches for porting to surefire > 2.17
- Workaround bugs in maven-plugin-plugin due to having java 8 code on the
  classpath when extracting mojo descriptors

* Mon Jul 25 2016 Mat Booth <mat.booth@redhat.com> - 0.25.0-7.1
- Auto SCL-ise package for rh-eclipse46 collection

* Mon Jul 25 2016 Mat Booth <mat.booth@redhat.com> - 0.25.0-7
- Remove incomplete SCL macros

* Thu Jun 30 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.25.0-6
- Add missing requires on maven-plugin-testing-harness

* Thu Jun 30 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.25.0-5
- Require full xmvn

* Wed Jun 15 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.25.0-4
- Add missing requires on maven-source-plugin

* Fri Apr 22 2016 Mat Booth <mat.booth@redhat.com> - 0.25.0-3
- Require newer ECJ with correct aliases

* Thu Apr 21 2016 Mat Booth <mat.booth@redhat.com> - 0.25.0-2
- Non-bootstrap build against Eclipse Neon

* Wed Apr 20 2016 Mat Booth <mat.booth@redhat.com> - 0.25.0-1
- Update to latest upstream release
- Full bootstrap mode due to incompatibility with Eclipse Mars

* Thu Apr 14 2016 Mat Booth <mat.booth@redhat.com> - 0.23.0-17
- Fix build against new maven-archiver, which removed some deprecated methods
  that tycho was using

* Tue Mar 15 2016 Mat Booth <mat.booth@redhat.com> - 0.23.0-16
- Update to latest fp-p2 snapshot

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.23.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jan 25 2016 Mat Booth <mat.booth@redhat.com> - 0.23.0-14
- Updates to latest version of fedoraproject-p2.
- fedoraproject-p2: Fix a concurrent modification exception when feature
  plugins have circular deps

* Mon Jan 11 2016 Roland Grunberg <rgrunber@redhat.com> - 0.23.0-13
- Updated to latest version of fedoraproject-p2.
- fedoraproject-p2: Correctly handle splitting virtual packages.

* Mon Jan  4 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.23.0-12
- Update for maven-surefire 2.19.1

* Mon Oct 26 2015 Roland Grunberg <rgrunber@redhat.com> - 0.23.0-11
- Fix bug in org.eclipse.tycho.surefire.junit4 provider.

* Tue Oct 20 2015 Roland Grunberg <rgrunber@redhat.com> - 0.23.0-10
- Update to work with maven-surefire 2.19.

* Thu Aug 27 2015 Roland Grunberg <rgrunber@redhat.com> - 0.23.0-9
- fedoraproject-p2: Enable support for p2 Droplets.

* Tue Jul 28 2015 Roland Grunberg <rgrunber@redhat.com> - 0.23.0-8
- fedoraproject-p2: Single IU resolving requirements with multiple matches.

* Fri Jul 17 2015 Roland Grunberg <rgrunber@redhat.com> - 0.23.0-7
- fedoraproject-p2: Remove host localization fragments from reactor units.

* Tue Jun 30 2015 Mat Booth <mat.booth@redhat.com> - 0.23.0-6
- Fix bootstrap build
- fedoraproject-p2: Allow xmvn-p2-installer to work in bootstrap mode

* Thu Jun 25 2015 Roland Grunberg <rgrunber@redhat.com> - 0.23.0-5
- fedoraproject-p2: Do not generate requires for fragments.
- Update to work with maven-surefire 2.18.

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.23.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jun 09 2015 Mat Booth <mat.booth@redhat.com> - 0.23.0-3
- Fix bootstrap build

* Tue Jun  9 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.23.0-2
- Port to Plexus Archiver 3.0.1

* Fri Jun 05 2015 Mat Booth <mat.booth@redhat.com> - 0.23.0-1
- Update to 0.23.0 release
- Allow tycho-bootstrap.sh to work with "set -e" to fail faster
  and see errors more easily

* Sat May 30 2015 Alexander Kurtakov <akurtako@redhat.com> 0.22.0-18
- Fix build with no tomcat servlet.

* Thu May 07 2015 Mat Booth <mat.booth@redhat.com> - 0.22.0-17
- Add org.tukaani.xz to tycho-bundles-external

* Tue Apr 28 2015 Roland Grunberg <rgrunber@redhat.com> - 0.22.0-16
- Fix resolution issues when upstream version in local repository.
- Resolves: rhbz#1216170

* Thu Apr 23 2015 Mat Booth <mat.booth@redhat.com> - 0.22.0-15
- fedoraproject-p2: Add support for archful dropins

* Mon Apr 20 2015 Roland Grunberg <rgrunber@redhat.com> - 0.22.0-14
- Handle possible changes to metadata namespace (ns[0-9]).

* Fri Apr 17 2015 Roland Grunberg <rgrunber@redhat.com> - 0.22.0-13
- fedoraproject-p2: Subpackages '*-tests' should not be in dropins.

* Sun Mar 29 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.22.0-12
- Port to Jetty 9.3.0

* Thu Feb  5 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.22.0-11
- fedoraproject-p2: Fix support for shallow dropin directory layout

* Wed Feb  4 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.22.0-10
- fedoraproject-p2: Bump BREE to JavaSE-1.8
- fedoraproject-p2: Fix installing of virtual bundles provided by p2.inf

* Wed Jan 28 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.22.0-9
- fedoraproject-p2: Allow installation of bundles not built with tycho

* Mon Jan 19 2015 Roland Grunberg <rgrunber@redhat.com> - 0.22.0-8
- Introduce basic SCL support.
- Minor changes for bootstrap build.
- Suppress failed lookups on non-existing paths in scripts.
- Explicitly depend on org.hamcrest.core where necessary.

* Thu Dec 11 2014 Mat Booth <mat.booth@redhat.com> - 0.22.0-7
- fedoraproject-p2: Fix for bundles containing underscores

* Wed Dec 10 2014 Mat Booth <mat.booth@redhat.com> - 0.22.0-6
- fedoraproject-p2: Update to latest snapshot

* Wed Dec 10 2014 Roland Grunberg <rgrunber@redhat.com> - 0.22.0-5
- Rebuild to pick up arch-independent ECF bundle locations.

* Mon Dec 08 2014 Roland Grunberg <rgrunber@redhat.com> - 0.22.0-4
- fedoraproject-p2: Permit installation of tycho-generated source features.

* Thu Dec  4 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.22.0-3
- Non-bootstrap build

* Thu Dec  4 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.22.0-2.1
- fedoraproject-p2: Add support for installation into SCLs
- Bootstrap build

* Thu Dec 04 2014 Mat Booth <mat.booth@redhat.com> - 0.22.0-2
- Fix osgi.jar symlink when in eclipse-bootstrap mode
- Remove no longer needed workaround for rhbz#1139180
- Tidy up and remove unneeded R/BRs
- Also reduce number of changes needed to SCL-ise package

* Mon Dec 01 2014 Mat Booth <mat.booth@redhat.com> - 0.22.0-1
- Update to tagged release

* Thu Nov 27 2014 Roland Grunberg <rgrunber@redhat.com> - 0.22.0-0.1.gitb1051d
- Update to 0.22.0 pre-release.

* Thu Nov 27 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.21.0-23
- fedoraproject-p2: Obtain SCL roots by parsing Java conf files
- fedoraproject-p2: Add support for installing into SCL root

* Thu Nov 27 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.21.0-22
- Install p2-install.sh script in java-utils/

* Thu Nov 27 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.21.0-21
- fedoraproject-p2: Implement installer application

* Tue Nov 25 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.21.0-20
- fedoraproject-p2: Update to latest snapshot (SCL improvements)

* Thu Nov 06 2014 Mat Booth <mat.booth@redhat.com> - 0.21.0-19
- fedoraproject-p2: Fix occasionally failing to generate metadata

* Tue Oct 28 2014 Roland Grunberg <rgrunber@redhat.com> - 0.21.0-18
- Fixes to bootstrap build.
- Package com.ibm.icu (icu4j-eclipse) for bootstrap build.
- Resolves: rhbz#1129801

* Thu Oct 09 2014 Mat Booth <mat.booth@redhat.com> - 0.21.0-17
- fedoraproject-p2: Fix incorrect metadata generation bugs

* Tue Oct 07 2014 Mat Booth <mat.booth@redhat.com> - 0.21.0-16
- fedoraproject-p2: Update to latest snapshot

* Thu Oct 02 2014 Roland Grunberg <rgrunber@redhat.com> - 0.21.0-15
- Update to build against plexus-archiver 2.6.

* Thu Sep 25 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.21.0-14
- fedoraproject-p2: Fix requires generation bug

* Wed Sep 24 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.21.0-13
- fedoraproject-p2: Allow installation of source bundles

* Mon Sep 22 2014 Roland Grunberg <rgrunber@redhat.com> - 0.21.0-12
- Add Fedora system repos to target definition resolver.
- Look for any IU if IU/Version query fails in target definition resolver.

* Fri Sep 12 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.21.0-11
- fedoraproject-p2: Allow installing the same symlink into separate dropins

* Wed Sep 10 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.21.0-10
- Fix tycho-bundles-external-manifest.txt generation

* Wed Sep 10 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.21.0-9
- fedoraproject-p2: Fix self-dependencies failing builds

* Tue Sep 9 2014 Roland Grunberg <rgrunber@redhat.com> - 0.21.0-8
- Make debundling more resilient to changes.
- fedoraproject-p2: Update to latest (Fix metapackage merging).

* Mon Sep  8 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.21.0-8
- fedoraproject-p2: Import XMvn P2 plugin
- fedoraproject-p2: Fix NPE bug
- fedoraproject-p2: Avoid extracting tycho-bundles-external.zip

* Fri Sep 05 2014 Roland Grunberg <rgrunber@redhat.com> - 0.21.0-7
- Debundle tycho-bundles-external and tycho-standalone-p2-director.
- Resolves: rhbz#789272

* Thu Sep 04 2014 Roland Grunberg <rgrunber@redhat.com> - 0.21.0-6
- Use fedoraproject-p2 to do OSGi bundle discovery.

* Wed Sep 03 2014 Mat Booth <mat.booth@redhat.com> - 0.21.0-5
- Include eclipse features dir in custom resolver

* Wed Sep 03 2014 Roland Grunberg <rgrunber@redhat.com> - 0.21.0-4
- fedoraproject-p2: Do not regenerate IU metadata on every query.

* Thu Aug 28 2014 Mat Booth <mat.booth@redhat.com> - 0.21.0-3
- Perform non-bootstrap build
- Update running-env-only patch

* Wed Aug 27 2014 Roland Grunberg <rgrunber@redhat.com> - 0.21.0-2.1
- fedoraproject-p2: Fix issues with creation of feature IUs.
- fedoraproject-p2: Fix jar corruption bug.

* Thu Aug 21 2014 Roland Grunberg <rgrunber@redhat.com> - 0.21.0-2
- Integrate fedoraproject-p2 into Tycho.

* Thu Jul 24 2014 Roland Grunberg <rgrunber@redhat.com> - 0.21.0-1
- Update to 0.21.0 Release.

* Fri Jul 11 2014 Mat Booth <mat.booth@redhat.com> - 0.20.0-18
- Allow director plugin to only assemble products for the current arch
- Drop some unneeded BR/Rs on surefire (maven-local pulls these in)

* Wed Jul 02 2014 Roland Grunberg <rgrunber@redhat.com> - 0.20.0-17
- Return non-existant expected local path when resolution fails.
- Resolves: rhbz#1114120

* Fri Jun 27 2014 Roland Grunberg <rgrunber@redhat.com> - 0.20.0-16
- Tycho should always delegate artifact resolution to Maven.

* Wed Jun 25 2014 Alexander Kurtakov <akurtako@redhat.com> 0.20.0-15
- Non-bootstrap build now that aarch64 is done.

* Tue Jun 24 2014 Roland Grunberg <rgrunber@redhat.com> - 0.20.0-14.1
- Add swt aarch64 fragment to bootstrap repo.

* Tue Jun 24 2014 Alexander Kurtakov <akurtako@redhat.com> 0.20.0-14
- Full bootstrap build for secondary archs.

* Thu Jun 12 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.20.0-13
- Restore runtime dependencies on XMvn

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Jun  3 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.20.0-11
- Skip intermediary build in non-bootstrap mode
- Resolves: rhbz#1103839
- Remove unneeded XMvn bits

* Fri May 30 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.20.0-10
- Fix runtime dependencies on XMvn in POMs
- Use custom Plexus config to lookup XMvn classes
- Lookup Aether WorkspaceReader using role hint "ide"

* Thu May 29 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.20.0-9
- Don'n install duplicate Maven metadata for sisu-equinox

* Wed May 21 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.20.0-8
- Use .mfiles generated during build

* Fri May 16 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.20.0-7
- Add support for XMvn 2.0

* Tue May 13 2014 Alexander Kurtakov <akurtako@redhat.com> 0.20.0-6
- Make tycho copy licence feature to the system repo.

* Wed Apr 30 2014 Alexander Kurtakov <akurtako@redhat.com> 0.20.0-5
- Non-bootstrap build.

* Tue Apr 29 2014 Alexander Kurtakov <akurtako@redhat.com> 0.20.0-4
- Organize patches.

* Tue Apr 22 2014 Roland Grunberg <rgrunber@redhat.com> - 0.20.0-3
- Add support for compact profiles (Bug 1090003).

* Wed Apr 02 2014 Roland Grunberg <rgrunber@redhat.com> - 0.20.0-2
- Non-bootstrap build.

* Thu Mar 27 2014 Roland Grunberg <rgrunber@redhat.com> - 0.20.0-1.1
- Update to Eclipse Luna (4.4).

* Mon Mar 24 2014 Roland Grunberg <rgrunber@redhat.com> - 0.20.0-1
- Update to 0.20.0 Release.

* Wed Mar 12 2014 Roland Grunberg <rgrunber@redhat.com> - 0.19.0-11
- Respect %%{eclipse_bootstrap} flag in tycho-bootstrap.sh.
- Update Eclipse bootstrap cache.
- Fix Equinox Launcher usage logic in copy-platform-all.

* Thu Mar 06 2014 Roland Grunberg <rgrunber@redhat.com> - 0.19.0-10
- Non-bootstrap build.

* Thu Mar 06 2014 Roland Grunberg <rgrunber@redhat.com> - 0.19.0-9.1
- Do not check %%{_libdir}/eclipse plugins/features folders twice.

* Wed Feb 26 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.19.0-9
- Improve logging and error handling fop copy-platform-all

* Wed Jan 15 2014 Roland Grunberg <rgrunber@redhat.com> - 0.19.0-8
- Perform a pure bootstrap build.
- Fix issues with bootstrap build.

* Thu Jan 09 2014 Roland Grunberg <rgrunber@redhat.com> - 0.19.0-7
- Fix bootstrap build.

* Mon Jan  6 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.19.0-6
- Fix usage of %%add_maven_depmap for zip files
- Resolves: rhbz#1004310

* Mon Dec 9 2013 Alexander Kurtakov <akurtako@redhat.com> 0.19.0-5
- Switch to using %%mvn_build.
- Update BR/R names.
- Adapt to asm5.

* Thu Nov 21 2013 Roland Grunberg <rgrunber@redhat.com> - 0.19.0-4
- Return expected reactor cache location when XMvn resolution fails.

* Wed Nov 20 2013 Roland Grunberg <rgrunber@redhat.com> - 0.19.0-3
- Bump release for rebuild (Bug 1031769).

* Mon Nov 18 2013 Roland Grunberg <rgrunber@redhat.com> - 0.19.0-2
- Reduce length of file lock name when file is in build directory.

* Thu Oct 24 2013 Roland Grunberg <rgrunber@redhat.com> - 0.19.0-1
- Update to 0.19.0 Release.

* Fri Oct 04 2013 Roland Grunberg <rgrunber@redhat.com> - 0.18.1-7
- Do not use XMvn internals (Bug 1015038).

* Thu Oct 3 2013 Krzysztof Daniel <kdaniel@redhat.com> 0.18.1-6
- Adjust to latest Xmvn (workaround for 1015038).

* Mon Sep  9 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.18.1-5
- Add workaround for rhbz#1004310

* Tue Jul 30 2013 Roland Grunberg <rgrunber@redhat.com> - 0.18.1-4
- Improve artifact resolution using XMvn Resolver. (Bug 986900)

* Mon Jul 29 2013 Roland Grunberg <rgrunber@redhat.com> - 0.18.1-3
- Fix Tycho file locking to work in Fedora.
- Skip validateConsistentTychoVersion by default. (Bug 987271)

* Wed Jul 24 2013 Roland Grunberg <rgrunber@redhat.com> - 0.18.1-2
- Non-bootstrap build.

* Wed Jul 24 2013 Roland Grunberg <rgrunber@redhat.com> - 0.18.1-1.1
- Update to use Eclipse Aether.
- Use MavenSession and Plexus to determine state.
- Fix bootstrap build.

* Thu Jul 18 2013 Roland Grunberg <rgrunber@redhat.com> 0.18.1-1
- Make changes to ensure intermediary build succeeds.
- Remove %%Patch6 in favour of call to sed.

* Thu Jul 18 2013 Krzysztof Daniel <kdaniel@redhat.com> 0.18.1-1
- Update to 0.18.1.

* Tue Jul 16 2013 Roland Grunberg <rgrunber@redhat.com> - 0.18.0-5
- Look for maven artifacts using XMvn Resolver.

* Tue Jul 9 2013 Roland Grunberg <rgrunber@redhat.com> 0.18.0-4
- Update to use maven-surefire 2.15 API.

* Fri Jul 5 2013 Alexander Kurtakov <akurtako@redhat.com> 0.18.0-3
- Use _jnidir too when building local p2 repo.

* Thu Jun 6 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.18.0-2
- Add Requires on plugins present in Maven super POM
- Resolves: rhbz#971301

* Tue May 28 2013 Roland Grunberg <rgrunber@redhat.com> 0.18.0-1
- Update to 0.18.0 Release.

* Thu Apr 11 2013 Roland Grunberg <rgrunber@redhat.com> 0.17.0-1
- Fix bootstrap build for potential future use.

* Tue Apr 2 2013 Roland Grunberg <rgrunber@redhat.com> 0.17.0-1
- Update to 0.17.0 Release.

* Mon Mar 18 2013 Roland Grunberg <rgrunber@redhat.com> 0.17.0-0.11.git3351b1
- Non-bootstrap build.

* Mon Mar 18 2013 Krzysztof Daniel <kdaniel@redhat.com> 0.17.0-0.10.git3351b1
- Merge mizdebsk patch with existing custom resolver patch.

* Mon Mar 18 2013 Krzysztof Daniel <kdaniel@redhat.com> 0.17.0-0.9.git3351b1
- Move the patch into better place.

* Mon Mar 18 2013 Krzysztof Daniel <kdaniel@redhat.com> 0.17.0-0.8.git3351b1
- Non-bootstrap build.

* Mon Mar 18 2013 Krzysztof Daniel <kdaniel@redhat.com> 0.17.0-0.7.git3351b1
- Commit the patch.

* Mon Mar 18 2013 Krzysztof Daniel <kdaniel@redhat.com> 0.17.0-0.6.git3351b1
- Use plexus to instantiate workspace reader.

* Sun Mar 17 2013 Roland Grunberg <rgrunber@redhat.com> 0.17.0-0.5.git3351b1
- Non-bootstrap build.

* Fri Mar 15 2013 Roland Grunberg <rgrunber@redhat.com> 0.17.0-0.4.git3351b1
- Update bootstrapped build for 0.17.0-SNAPSHOT to work against 0.16.0.
- Update to Plexus Compiler 2.2 API.

* Thu Feb 28 2013 Roland Grunberg <rgrunber@redhat.com> 0.17.0-0.3.git3351b1
- Update to using Jetty 9 API.

* Mon Feb 25 2013 Roland Grunberg <rgrunber@redhat.com> 0.17.0-0.2.git3351b1
- Set the global default execution environment to JavaSE-1.6.
- Patch clean-up.

* Mon Feb 25 2013 Krzysztof Daniel <kdaniel@redhat.com> 0.17.0-0.1.git3351b1
- Update to latest upstream.
- RHBZ#915194 - API changed in maven-surefire

* Wed Feb 6 2013 Roland Grunberg <rgrunber@redhat.com> 0.16.0-21
- Non-bootstrap build.

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 0.16.0-20.2
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Wed Feb 6 2013 Roland Grunberg <rgrunber@redhat.com> 0.16.0-20.1
- Change BR/R on maven to maven-local for XMvn support.
- Build bootstrapped to fix missing Fedora Maven class.

* Thu Jan 24 2013 Roland Grunberg <rgrunber@redhat.com> 0.16.0-20
- Use TYCHO_MVN_{LOCAL,RPMBUILD} to determine how maven was called.
- Update to maven-surefire 2.13.

* Thu Dec 20 2012 Roland Grunberg <rgrunber@redhat.com> 0.16.0-19
- Fix upstream Bug 361204.

* Mon Dec 3 2012 Roland Grunberg <rgrunber@redhat.com> 0.16.0-18
- Add support for more flexible OSGi bundle paths.
- Use OSGi Requires instead of package name.
- Expand Requires to include the Eclipse platform.

* Mon Nov 19 2012 Roland Grunberg <rgrunber@redhat.com> 0.16.0-17
- Make additional changes to get Tycho building bootstrapped.

* Mon Nov 5 2012 Roland Grunberg <rgrunber@redhat.com> 0.16.0-16
- Add capability to build without depending on Tycho or Eclipse.

* Sat Oct 20 2012 Roland Grunberg <rgrunber@redhat.com> 0.16.0-15
- Package org.eclipse.osgi and org.eclipse.jdt.core.

* Fri Oct 19 2012 Roland Grunberg <rgrunber@redhat.com> 0.16.0-14
- Update to finalized 0.16.0 Release.

* Wed Oct 17 2012 Roland Grunberg <rgrunber@redhat.com> 0.16.0-13
- Build Tycho properly in one RPM build.
- Update to 0.16.0 Release.

* Thu Oct 11 2012 Roland Grunberg <rgrunber@redhat.com> 0.16.0-12.d7f885
- Non-bootstrap build.

* Thu Oct 11 2012 Roland Grunberg <rgrunber@redhat.com> 0.16.0-11.1.d7f885
- Remove dependence on eclipse by use of self-bundled equinox launcher.

* Wed Oct 10 2012 Roland Grunberg <rgrunber@redhat.com> 0.16.0-11.d7f885
- copy-platform-all should make symlinked jars from %%{_javadir} unique.
- Non-bootstrap build (reset the %%bootstrap flag properly).

* Mon Oct 8 2012 Krzysztof Daniel <kdaniel@redhat.com> 0.16.0-10.d7f885
- Non-bootstrap build.

* Mon Oct 8 2012 Krzysztof Daniel <kdaniel@redhat.com> 0.16.0-9.1.d7f885
- Filter out OSGi dependencies.

* Thu Oct 4 2012 Roland Grunberg <rgrunber@redhat.com> 0.16.0-9.d7f885
- Non-bootstrap build.

* Thu Oct 4 2012 Roland Grunberg <rgrunber@redhat.com> 0.16.0-8.1.d7f885
- Fix Bug in overriding of BREE to JavaSE-1.6.

* Wed Oct 3 2012 Roland Grunberg <rgrunber@redhat.com> 0.16.0-8.d7f885
- Non-bootstrap build.

* Wed Oct 3 2012 Roland Grunberg <rgrunber@redhat.com> 0.16.0-7.1.d7f885
- Update to latest 0.16.0 SNAPSHOT.
- First attempts to build without cyclic dependency to JDT.

* Mon Aug 27 2012 Roland Grunberg <rgrunber@redhat.com> 0.16.0-7.df2c35
- Non bootstrap-build.

* Mon Aug 27 2012 Roland Grunberg <rgrunber@redhat.com> 0.16.0-6.1.df2c35
- Add BR/R on explicit dependency objectweb-asm4.
- Use consistent whitespace in specfile.

* Fri Aug 24 2012 Roland Grunberg <rgrunber@redhat.com> 0.16.0-6.df2c35
- Non-bootstrap build.

* Thu Aug 23 2012 Roland Grunberg <rgrunber@redhat.com> 0.16.0-5.1.df2c35
- Set BREE to at least JavaSE-1.6 for all eclipse packaging types.
- Remove unneeded workaround for JSR14 incompatibility of JDK 1.7.

* Wed Aug 15 2012 Roland Grunberg <rgrunber@redhat.com> 0.16.0-5.df2c35
- Non-bootstrap build.

* Mon Aug 13 2012 Roland Grunberg <rgrunber@redhat.com> 0.16.0-4.1.df2c35
- Correctly reference objectweb-asm4 and fix local mode resolution bug.
- Update spec file to honour new java packaging guidelines.

* Thu Aug 9 2012 Roland Grunberg <rgrunber@redhat.com> 0.16.0-4.df2c35
- Non-bootstrap build.

* Thu Aug 9 2012 Roland Grunberg <rgrunber@redhat.com> 0.16.0-3.1.df2c35
- Add tycho.local.keepTarget flag to bypass ignoring environments.

* Thu Aug 9 2012 Krzysztof Daniel <kdaniel@redhat.com> 0.16.0-3.df2c35
- Non-bootstrap build.

* Thu Aug 9 2012 Krzysztof Daniel <kdaniel@redhat.com> 0.16.0-2.1.df2c35
- Use recommended %%add_maven_depmap. 

* Thu Aug 9 2012 Krzysztof Daniel <kdaniel@redhat.com> 0.16.0-2.df2c35
- Non-bootstrap build.

* Thu Aug 9 2012 Krzysztof Daniel <kdaniel@redhat.com> 0.16.0-1.2.df2c35
- Properly change bootstrap flag.
- Add some git ignores.

* Thu Aug 9 2012 Krzysztof Daniel <kdaniel@redhat.com> 0.16.0-1.1.df2c35
- Install missing tycho-standalone-p2-director.zip.

* Thu Aug 2 2012 Roland Grunberg <rgrunber@redhat.com> 0.16.0-1.df2c35
- Update to 0.16.0 SNAPSHOT.

* Tue Jul 31 2012 Roland Grunberg <rgrunber@redhat.com> 0.15.0-3
- Non-bootstrap build.

* Tue Jul 31 2012 Roland Grunberg <rgrunber@redhat.com> 0.15.0-2.1
- Ignore defined environments in local mode.

* Mon Jul 30 2012 Roland Grunberg <rgrunber@redhat.com> 0.15.0-2
- Non-bootstrap build.

* Mon Jul 30 2012 Roland Grunberg <rgrunber@redhat.com> 0.15.0-1.1
- Fix copy-platform-all script to properly link %%{_datadir}/eclipse jars.

* Thu Jul 26 2012 Roland Grunberg <rgrunber@redhat.com> 0.15.0-1
- Update to 0.15.0.
- Set BREE to at least JavaSE-1.6 for Eclipse feature bundles.

* Wed Jul 25 2012 Roland Grunberg <rgrunber@redhat.com> 0.14.1-7
- Non-bootstrap build.

* Mon Jul 23 2012 Roland Grunberg <rgrunber@redhat.com> 0.14.1-6
- Detect OSGi jars using presence of Bundle-SymbolicName entry (BZ #838513).

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Roland Grunberg <rgrunber@redhat.com> 0.14.1-5
- Non-bootstrap build.

* Tue May 29 2012 Roland Grunberg <rgrunber@redhat.com> 0.14.1-4.1
- Fix Tycho Surfire to run Eclipse test bundles.
- Implement automatic creation of a system p2 repository.
- Allow building SWT fragments (BZ #380934).

* Wed May 23 2012 Roland Grunberg <rgrunber@redhat.com> 0.14.1-4
- Non-bootstrap build.

* Thu May 17 2012 Roland Grunberg <rgrunber@redhat.com> 0.14.1-3.1
- Set BREE to be at least JavaSE-1.6 for Eclipse OSGi bundles.

* Wed May 16 2012 Roland Grunberg <rgrunber@redhat.com> 0.14.1-3
- Non-bootstrap build.

* Wed Apr 25 2012 Roland Grunberg <rgrunber@redhat.com> 0.14.1-2.1
- Implement a custom resolver when running in local mode.
- Use upstream solution for BZ #372395 to fix the build.

* Wed Apr 4 2012 Roland Grunberg <rgrunber@redhat.com> 0.14.1-2
- Non-bootstrap build.

* Tue Mar 27 2012 Roland Grunberg <rgrunber@redhat.com> 0.14.1-1.1
- Add missing tycho-testing-harness to be packaged.
- Use %%{_eclipse_base} from eclipse-platform.

* Fri Mar 9 2012 Roland Grunberg <rgrunber@redhat.com> 0.14.1-1
- Update to 0.14.1 upstream tag.
- Allow building against maven-surefire 2.12 (instead of 2.10).
- Stop symlinking o.e.osgi and o.e.jdt.core into the m2 cache.

* Thu Feb 16 2012 Roland Grunberg <rgrunber@redhat.com> 0.14.0-4
- Non-bootstrap build.

* Tue Feb 14 2012 Roland Grunberg <rgrunber@redhat.com> 0.14.0-3
- Update to 0.14.0 upstream tag.

* Thu Feb 9 2012 Roland Grunberg <rgrunber@redhat.com> 0.14.0-2
- Non-bootstrap build.

* Wed Feb 01 2012 Roland Grunberg <rgrunber@redhat.com> - 0.14.0-1
- Update to 0.14.0.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri May 27 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0.12.0-0.1.a74b1717
- Update to new version do bootstrap from scratch

* Fri May 6 2011 Alexander Kurtakov <akurtako@redhat.com> 0.10.0-3
- Non-bootstrap build.

* Tue May  3 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0.10.0-2
- Add README and make build more silent

* Tue Mar 29 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0.10.0-1
- First bootstrapped version
