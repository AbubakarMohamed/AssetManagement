from django.shortcuts import render, redirect, get_object_or_404
from .models import Asset, Lend, Maintenance
from .forms import LendForm, MaintenanceForm, AddAssetForm
from .forms import ReturnAssetForm
from django.http import JsonResponse
def index(request):
    return render(request,'assets/index.html')

def home(request):
    if request.method == 'POST':
        form = AddAssetForm(request.POST)
        if form.is_valid():
            asset = form.save(commit=False)
            asset.available_quantity = asset.total_quantity  # Ensure available quantity matches total quantity initially
            asset.save()
            return redirect('home')
    else:
        form = AddAssetForm()
    
    assets = Asset.objects.all()
    lent_assets = Lend.objects.filter(returned_date__isnull=True)
    context = {
        'assets': assets,
        'lent_assets': lent_assets,
        'form': form,
    }
    return render(request, 'assets/home.html', context)




def track(request):
    if request.method == 'POST':
        form = LendForm(request.POST)
        if form.is_valid():
            lend = form.save()
            asset = lend.asset
            asset.available_quantity -= lend.quantity
            asset.save()
            return redirect('home')
    else:
        form = LendForm()
    return render(request, 'assets/track.html', {'form': form})




def maintenance(request):
    if request.method == 'POST':
        form = MaintenanceForm(request.POST)
        if form.is_valid():
            maintenance = form.save(commit=False)
            asset = maintenance.asset
            if maintenance.is_fixed:
                asset.available_quantity += maintenance.quantity
                asset.save()
                maintenance.delete()  # Remove the maintenance record if fixed
            else:
                maintenance.save()
            return redirect('maintenance')
    else:
        form = MaintenanceForm()
    
    maintenance_records = Maintenance.objects.filter(is_fixed=False)
    return render(request, 'assets/maintenance.html', {'form': form, 'maintenance_records': maintenance_records})


def fix_asset(request, maintenance_id):
    maintenance = get_object_or_404(Maintenance, id=maintenance_id)
    if request.method == 'POST':
        form = MaintenanceForm(request.POST, instance=maintenance)
        if form.is_valid():
            maintenance = form.save(commit=False)
            if maintenance.is_fixed:
                asset = maintenance.asset
                asset.available_quantity += maintenance.quantity
                asset.save()
                maintenance.delete()  # Remove the maintenance record if fixed
            else:
                maintenance.save()
            return redirect('maintenance')
    else:
        form = MaintenanceForm(instance=maintenance)
    
    return render(request, 'assets/fix_asset.html', {'form': form, 'maintenance': maintenance})




def return_asset(request, lend_id):
    lend = get_object_or_404(Lend, id=lend_id)
    if request.method == 'POST':
        form = ReturnAssetForm(request.POST, instance=lend)
        if form.is_valid():
            quantity_good = form.cleaned_data['quantity_good']
            quantity_bad = form.cleaned_data['quantity_bad']
            
            if quantity_good + quantity_bad > lend.quantity:
                form.add_error(None, "Returned quantities cannot exceed lent quantity")
            else:
                lend.returned_date = form.cleaned_data['returned_date']
                lend.condition = form.cleaned_data['condition']
                lend.quantity_good = quantity_good
                lend.quantity_bad = quantity_bad
                
                asset = lend.asset
                asset.available_quantity += quantity_good
                
                if quantity_bad > 0:
                    Maintenance.objects.create(asset=asset, quantity=quantity_bad)
                
                asset.save()
                lend.save()
                return redirect('home')
    else:
        form = ReturnAssetForm(instance=lend)
    
    return render(request, 'assets/return_asset.html', {'form': form, 'lend': lend})


def get_asset_ids(request):
    asset_id = request.GET.get('asset_id', None)
    if asset_id:
        ids = Asset.objects.filter(id=asset_id).values('id', 'unique_id')
        return JsonResponse({'ids': list(ids)})
    return JsonResponse({'ids': []})