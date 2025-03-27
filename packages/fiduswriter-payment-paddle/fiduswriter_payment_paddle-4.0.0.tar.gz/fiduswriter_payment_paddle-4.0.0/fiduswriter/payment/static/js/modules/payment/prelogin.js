export class PaymentPrelogin {
    constructor({page}) {
        this.preloginPage = page
    }

    init() {
        this.preloginPage.footerLinks.push({
            text: gettext("Pricing"),
            link: "/pricing/"
        })
    }
}
