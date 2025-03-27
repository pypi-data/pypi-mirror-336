import {Dialog} from "../common"

export class PaymentDocumentsOverview {
    constructor(overview) {
        this.overview = overview
    }

    init() {
        this.overview.goToNewDocumentAction = this.overview.goToNewDocument
        this.overview.goToNewDocument = (...args) => {
            this.overview.app.getSubscription().then(() => {
                if (
                    this.overview.app.subscription.staff ||
                    this.overview.app.subscription.subscribed ||
                    this.overview.documentList.length < 2
                ) {
                    this.overview.goToNewDocumentAction(...args)
                } else {
                    const dialog = new Dialog({
                        title: gettext("Subscription warning"),
                        body: `<p>${gettext("You have run out of free documents. Sign up for a subscription to create more documents.")}</p>`,
                        buttons: [
                            {
                                text: gettext("Go to subscription page"),
                                classes: "fw-dark",
                                click: () => {
                                    dialog.close()
                                    this.overview.app.goTo("/payment/")
                                }
                            },
                            {type: "close"}
                        ]
                    })
                    dialog.open()
                }
            })
        }
    }
}
