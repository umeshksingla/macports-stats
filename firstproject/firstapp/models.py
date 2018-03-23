import uuid
import re

from django.contrib.postgres.fields import JSONField
from django.core.exceptions import ObjectDoesNotExist
from django.db import models

MAX_LENGTH = 255
ERROR = 1
SUCCESS = 0


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)


class User(models.Model):
    user_uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class PortIndex(models.Model):
    data = JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        print("Updating portindex ...")
        for port in self.data:

            try:
                name = port['name']
            except KeyError:
                name = NULL

            keys = ['version', 'revision', 'portdir', 'homepage', \
                'epoch', 'platforms', 'license', 'variants', 'description', \
                'long_description']

            defaults={}

            for key in keys:
                if key in port.keys():
                    defaults[key] = port[key]
                else:
                    defaults[key] = ""
            try:
                categories = port['categories'].split()
            except KeyError:
                categories = ""
            try:
                maintainers = re.findall(r"{.*?}|\w+", port["maintainers"])
            except KeyError:
                maintainers = ""

            try:
                defaults['exists'] = True
                p, created = Port.objects.update_or_create(
                    name=name,
                    defaults=defaults
                )

                for category in categories:
                    c, created = Category.objects.get_or_create(name=category)
                    p.categories.add(c)

                for maintainer in maintainers:
                    if maintainer == 'nomaintainer':
                        continue
                    elif maintainer == 'openmaintainer':
                        p.is_open_maintainer = True
                        p.save()
                    else:
                        m, created = Maintainer.objects.get_or_create(
                            github_handle=maintainer,)
                        p.maintainers.add(m)
            except ObjectDoesNotExist:
                print("Updating portindex unsuccessful.")
                return ERROR
        print("Updating portindex successful.")
        return SUCCESS


class Submission(models.Model):
    data = JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        try:
            user = User.objects.get(user_uuid=self.data['id'])
        except:
            user = User(user_uuid=self.data['id'])
            user.save()
        InstalledPort.populate(user, self.data['active_ports'])
        OsStatistic.populate(user, self.data['os'])


class Category(models.Model):
    name = models.CharField(
        unique=True,
        max_length=MAX_LENGTH,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']


class Maintainer(models.Model):
    github_handle = models.CharField(
        unique=True,
        max_length=MAX_LENGTH,
        null=True,
    )
    # TODO: handle @macports.org emails separately
    email = models.CharField(
        unique=True,
        max_length=MAX_LENGTH,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Port(models.Model):
    # TODO: update portindex using cronjob/buildbot/manual
    # Only add the updated/new ports. Go through all the
    # existing ports in this table, set exists=False,
    # and then exists=True if exist/add new ports from the 
    # current portindex

    name = models.CharField(
        null=False,
        unique=True,
        max_length=MAX_LENGTH,
    )

    exists = models.BooleanField(default=False)

    portdir = models.CharField(max_length=MAX_LENGTH)
    version = models.CharField(max_length=MAX_LENGTH)
    revision = models.IntegerField(default=0)
    epoch = models.CharField(
        default="0",
        max_length=MAX_LENGTH,
    )
    description = models.TextField(default="")
    long_description = models.TextField(default="")
    homepage = models.CharField(
        default="",
        max_length=MAX_LENGTH
    )

    license = models.CharField(max_length=MAX_LENGTH)
    variants = models.CharField(
        default="",
        max_length=MAX_LENGTH
    )
    platforms = models.CharField(default="",max_length=MAX_LENGTH)

    maintainers = models.ManyToManyField(Maintainer)
    is_open_maintainer = models.BooleanField(default=False)
    categories = models.ManyToManyField(Category)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']


class InstalledPort(models.Model):
    port = models.ForeignKey(
        Port,
        on_delete=models.CASCADE
    )
    installed_version = models.CharField(max_length=MAX_LENGTH)
    installed_variants = models.CharField(max_length=MAX_LENGTH)
    requested = models.BooleanField(default=False)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def populate(user, data):
        # TODO:
        # {'name': 'py36-psycopg2', 'version': '2.7.4_0', 'variants': 'postgresql10 +'}
        # for each in port:
        #     name = each['name']
        #     version = each['version']
        #     variants = each['variants']
        pass


class OsStatistic(models.Model):
    macports_version = models.CharField(max_length=MAX_LENGTH)
    osx_version = models.CharField(max_length=MAX_LENGTH)
    os_arch = models.CharField(max_length=MAX_LENGTH)
    os_platform = models.CharField(max_length=MAX_LENGTH)
    build_arch = models.CharField(max_length=MAX_LENGTH)
    xcode_version = models.CharField(max_length=MAX_LENGTH)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def populate(user, data):
        macports_version = data['macports_version']
        osx_version = data['osx_version']
        os_arch = data['os_arch']
        os_platform = data['os_platform']
        build_arch = data['build_arch']
        xcode_version = data['xcode_version']

        os_stat = OsStatistic(
            macports_version=macports_version,
            osx_version=osx_version,
            os_arch=os_arch,
            os_platform=os_platform,
            build_arch=build_arch,
            xcode_version=xcode_version,
            user=user,
        )
        os_stat.save()
