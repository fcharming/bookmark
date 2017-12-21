#coding:utf-8
from django import forms
from .models import Image
import urllib2
from django.core.files.base import ContentFile
from django.utils.text import slugify

class ImageCreateForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('title','url','description')
        widgets = {'url':forms.HiddenInput,}
        #widget是对于表单附加的控件

#clean_xx 用于检查数据是否符合规范
    def clean_url(self):
        url = self.cleaned_data['url']
        valid_extensions = ['jpg','jpeg']
        extension = url.rsplit('.',1)[1].lower()
        if extension not in valid_extensions:
            raise forms.ValidationError('The given url does not match valid extensions')
        return url

#复写save方法，保存时从url下载图片
    def save(self,force_insert=False,force_update=False,commit=True):
        image = super(ImageCreateForm, self).save(commit=False)
        image_url = self.cleaned_data['url']
        image_name = '{}.{}'.format(slugify(image.title),image_url.rsplit('.',1)[1].lower())
        request = urllib2.Request(image_url)
        response = urllib2.urlopen(request)
        image.image.save(image_name,ContentFile(response.read()),save=False)
        if commit:
            image.save()
        return image
