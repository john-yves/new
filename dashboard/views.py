from django.contrib import messages
from django.db import models
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, View, CreateView

from .forms import FamilyForm, AddKpiForm
from .models import Sector, KPI, Umuryango, Cell, Village
from django.db.models import Sum, Count, F


class DashboardView(ListView):
    model = Umuryango
    template_name = "dashboard/dashboard.html"

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        context['kpis'] = KPI.objects.all()
        # context['results'] = Result.objects.filter(sector=self.request.user.user_profile.sector)
        # context['achieved_results'] = Result.objects.filter(achieved=0, sector=self.request.user.user_profile.sector)
        # context['pending_results'] = Result.objects.filter(pending=0, sector=self.request.user.user_profile.sector)
        context['sectors'] = Sector.objects.all()

        context['achieved_total'] = Umuryango.objects.values('kpi__name', 'kpi_id') \
                                                     .annotate(achieved=Sum('achieved')) \
                                                     .annotate(target=Sum('target'))

        context['achieved_sector'] = Umuryango.objects.values('kpi__name', 'kpi_id')\
                                                  .annotate(achieved=Sum('achieved'))\
                                                  .annotate(target=Sum('target'))\
                                                  .filter(sector=self.request.user.user_profile.sector)


        # context['kpizose'] = Umuryang.objects.values('kpi__name', 'status').filter(status=False).annotate(Count('status'))
        # context['ibisigay'] = Umuryango.objects.filter(kpi__name='kpi_name').count()
        # Entry.objects.filter(authors__name=F('blog__name'))
        # context['ibisigaye'] = Umuryango.objects.filter(kpi__name=F('kpi1__name')).filter(status=True).distinct().count()
        # context['ibyakozw'] = Umuryango.objects.filter(status="True").filter(kpi__name=self.kwargs['kpi__name']).count()
        # context['ibyakozw'] = Umuryango.objects.values('kpi__name', 'kpi_id').filter(kpi__name=F('kpi__name'), status=True).annotate(status=Sum('status'))
        # context['ibisi'] = Umuryango.objects.values('kpi__name', 'kpi_id').filter(kpi__name='kpi__name', status=False).annotate(Count('status',distinct=True))





        return context


class KPIDetailView(DetailView):
    model = KPI
    template_name = "dashboard/kpi_detail.html"

    def get_context_data(self, **kwargs):
        context = super(KPIDetailView, self).get_context_data(**kwargs)
        context['kpis'] = KPI.objects.all()
        context['current_kpi'] = Umuryango.objects.filter(kpi_id=self.kwargs['pk'])\
                                          .values('kpi__name').annotate(targ=Sum('target'))\
                                          .annotate(achiev=Sum('achieved'))\
                                          .distinct()
        context['kpiname'] = Umuryango.objects.values('kpi__name').filter(kpi_id=self.kwargs['pk'])



        return context


class Ibyakozwe(ListView):
    model = KPI
    template_name = "umuryango/ibyakozwe.html"

    def get_context_data(self, **kwargs):
        context = super(Ibyakozwe, self).get_context_data(**kwargs)
        context['ibyakozwe'] = Umuryango.objects.filter(achieved=1).filter(kpi_id=self.kwargs['pk'])
        context['ibisigaye'] = Umuryango.objects.filter(achieved=0).filter(kpi_id=self.kwargs['pk'])

        context['ibyakozwe_sector'] = Umuryango.objects.filter(achieved=1, sector=self.request.user.user_profile.sector).filter(kpi_id=self.kwargs['pk'])
        context['ibisigaye_sector'] = Umuryango.objects.filter(achieved=0, sector=self.request.user.user_profile.sector).filter(kpi_id=self.kwargs['pk'])

        return context


class District_chartView(View):
    def get(self, request, pk):
        dataset = Umuryango.objects.values('kpi__name', 'sector__name').annotate(targ=Sum('target')) \
                           .annotate(achiev=Sum('achieved'))\
                           .filter(kpi_id=self.kwargs['pk'])\
                           .order_by('target')

        kpiname = Umuryango.objects.values('kpi__name').filter(kpi_id=self.kwargs['pk'])
        return render(request, 'dashboard/kpi_detail.html', {'dataset': dataset}, {'kpiname': kpiname})




class Sector_chartView(View):
    def get(self, request, pk):
        dataset = Umuryango.objects.values('kpi__name').annotate(targ=Sum('target')) \
                           .annotate(achiev=Sum('achieved')) \
                           .filter(kpi_id=self.kwargs['pk']) \
                           .filter(sector=self.request.user.user_profile.sector) \
                           .order_by('target')

        return render(request, 'dashboard/kpi_detail.html', {'dataset': dataset})

# view for add new family
class CreateFamily(CreateView):
    model = Umuryango
    form_class = FamilyForm
    template_name = 'umuryango/add_data_form.html'

    def form_valid(self, form):
        fam = form.save(commit=False)
        fam.save()
        messages.success(self.request, 'Family  created successfully.')
        return redirect('dashboard')


##############################view for loading cells based sector #########################################
def load_cells(request):
    sector_id = request.GET.get('sector')
    cells = Cell.objects.filter(sector_id=sector_id).order_by('name')
    return render(request, 'dashboard/dropdown.html', {'cells': cells})


###############################view for loading village Based on cells ####################################
def load_village(request):
    cell_id = request.GET.get('cell')
    villages = Village.objects.filter(cell_id=cell_id).order_by('name')
    return render(request, 'dashboard/dropdown.html', {'villages': villages})











# view for changing status to 1
def change_status(request, fam_id):
    Umuryango.objects.filter(sector=request.user.user_profile.sector, pk=fam_id).update(achieved=1)
    messages.success(request, 'Status changed Successfully.')
    return redirect('dashboard')


class AddKpi(CreateView):
    model = KPI
    form_class = AddKpiForm
    template_name = 'umuryango/add_data_form.html'

    def form_valid(self, form):
        kpiform = form.save(commit=False)
        kpiform.save()
        messages.success(self.request, 'KPI created successfully.')
        return redirect('dashboard')
