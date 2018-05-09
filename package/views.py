from django.shortcuts import redirect
from django.urls import reverse

from .models import Package
from django.views.generic import ListView
from django.contrib import messages
from monthdelta import monthdelta
import datetime


class PackageListView(ListView):
    template_name = 'package/package-list.html'
    context_object_name = 'packages'
    model = Package

    @staticmethod
    def get_locale_mount(mount: int):
        if mount == 1:
            return 'месяц'
        elif mount in [2, 3, 4]:
            return 'месяца'
        else:
            return 'месяцев'

    def post(self, request):
        """
        Покупка или продления тарифного плана
        :param request:
        """

        period = self.request.POST.get('period', False)
        package_id = self.request.POST.get('package', False)

        if not period:
            messages.error(request, 'Не выбран период', 'danger')
            return redirect(reverse('package:list'))

        package = Package.objects.get(id=package_id)
        need_money = float(package.price) * int(period)
        balance = round(float(self.request.user.profile.balance), 2)

        if self.request.user.profile.package == package:
            end_date = self.request.user.profile.package_end_date + monthdelta(int(period))
        else:
            end_date = datetime.datetime.now() + monthdelta(int(period))

        if balance < need_money:
            messages.error(
                request,
                'Для покупки пакета "{}" на период {} {} Вам не хватает {} у.е. Пополните Ваш баланс!'.format(
                    package.title, period, self.get_locale_mount(int(period)), need_money - balance,
                ),
                'danger'
            )
            return redirect(reverse('package:list'))

        self.request.user.profile.package = package
        self.request.user.profile.package_end_date = end_date
        self.request.user.save()

        messages.success(request, 'Пакет "{}" куплен. Нужно доделать покупку на период и списать бабло'.format(package.title))
        return redirect(reverse('package:list'))
