from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Wallet, WalletTransaction

@login_required
def wallet_dashboard(request):
    wallet = request.user.wallet
    transactions = wallet.transactions.order_by("-created_at")
    return render(request, "wallet/dashboard.html", {"wallet": wallet, "transactions": transactions})


@login_required
def add_money(request):
    if request.method == "POST":
        amount = request.POST.get("amount")
        if amount:
            wallet = request.user.wallet
            wallet.credit(float(amount))
            WalletTransaction.objects.create(wallet=wallet, amount=amount, transaction_type="CREDIT")
            return redirect("wallet_dashboard")
    return redirect("wallet_dashboard")


@login_required
def spend_money(request):
    if request.method == "POST":
        amount = request.POST.get("amount")
        if amount:
            wallet = request.user.wallet
            if wallet.debit(float(amount)):
                WalletTransaction.objects.create(wallet=wallet, amount=amount, transaction_type="DEBIT")
            else:
                return render(request, "wallet/dashboard.html", {
                    "wallet": wallet,
                    "transactions": wallet.transactions.order_by("-created_at"),
                    "error": "Insufficient balance!"
                })
    return redirect("wallet_dashboard")
