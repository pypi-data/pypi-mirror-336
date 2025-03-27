export class PaymentMenuItem {
    constructor(menu) {
        this.menu = menu
    }

    init() {
        this.menu.navItems.push({
            id: "payment",
            title: gettext("Modify subscription"),
            url: "/payment/",
            text: gettext("Subscription"),
            order: 100
        })
    }
}
