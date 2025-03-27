import {
    Dialog,
    activateWait,
    baseBodyTemplate,
    deactivateWait,
    ensureCSS,
    post,
    setDocTitle,
    whenReady
} from "../common"
import {FeedbackTab} from "../feedback"
import {SiteMenu} from "../menu"
import {advertisementTemplate} from "./templates"

export class PaymentPage {
    constructor({app, user}) {
        this.app = app
        this.user = user
    }

    init() {
        return this.app
            .getSubscription()
            .then(() => {
                ensureCSS([staticUrl("css/payment.css")])
                return whenReady()
            })
            .then(() => {
                this.render()
                const smenu = new SiteMenu(this.app, "payment")
                smenu.init()
            })
    }

    render() {
        const dom = document.createElement("body")
        dom.classList.add("payment")
        dom.innerHTML = baseBodyTemplate({
            contents: advertisementTemplate(
                Object.assign({}, this.app.paddleInfo, this.app.subscription)
            ),
            user: this.user,
            app: this.app
        })
        document.body = dom
        setDocTitle(gettext("Plan overview"), this.app)
        const feedbackTab = new FeedbackTab()
        feedbackTab.init()
        this.bind()
    }

    bind() {
        const subscriptionMonthlyButton = document.querySelector(
            ".subscription.monthly"
        )
        const subscriptionSixMonthsButton = document.querySelector(
            ".subscription.sixmonths"
        )
        const subscriptionAnnualButton = document.querySelector(
            ".subscription.annual"
        )

        subscriptionMonthlyButton.addEventListener("click", () =>
            this.handleClick("monthly")
        )
        subscriptionSixMonthsButton.addEventListener("click", () =>
            this.handleClick("sixmonths")
        )
        subscriptionAnnualButton.addEventListener("click", () =>
            this.handleClick("annual")
        )
    }

    updateSubscriptionInfo() {
        delete this.app.subscription
        activateWait()
        // Wait five seconds, then reload subscription status
        setTimeout(() => {
            deactivateWait()
            this.init()
        }, 5000)
    }

    handleClick(duration) {
        if (
            this.app.subscription.subscribed &&
            !this.app.subscription.subscription_end
        ) {
            if (this.app.subscription.subscribed === duration) {
                const dialog = new Dialog({
                    id: "figure-dialog",
                    title: gettext("Modify subscription"),
                    body: gettext(
                        "Please choose whether to update payment details or to cancel your subscription."
                    ),
                    buttons: [
                        {
                            text: gettext("Update payment details"),
                            classes: "fw-dark",
                            click: () =>
                                window.Paddle.Checkout.open({
                                    override: this.app.subscription.update_url,
                                    successCallback: () =>
                                        this.updateSubscriptionInfo()
                                })
                        },
                        {
                            text: gettext("Cancel subscription"),
                            classes: "fw-dark",
                            click: () =>
                                window.Paddle.Checkout.open({
                                    override: this.app.subscription.cancel_url,
                                    successCallback: () =>
                                        this.updateSubscriptionInfo()
                                })
                        },
                        {
                            type: "cancel"
                        }
                    ]
                })

                dialog.open()
            } else if (this.app.subscription.status === "trialing") {
                const dialog = new Dialog({
                    title: gettext("Plan change not possible"),
                    body: gettext(
                        "Unfortunately it is not possible to switch plans during the trial period."
                    ),
                    buttons: [{type: "close"}]
                })
                dialog.open()
            } else {
                const dialog = new Dialog({
                    id: "figure-dialog",
                    title: gettext("Switch subscription"),
                    body: gettext(
                        "Do you really want to switch your subscription type?"
                    ),
                    buttons: [
                        {
                            text: gettext("Yes"),
                            classes: "fw-dark",
                            click: () =>
                                post("/api/payment/update_subscription/", {
                                    plan_id: this.app.paddleInfo[duration].id
                                }).then(() => this.updateSubscriptionInfo())
                        },
                        {
                            type: "cancel"
                        }
                    ]
                })

                dialog.open()
            }
        } else {
            window.Paddle.Checkout.open({
                product: this.app.paddleInfo[duration].id,
                email: this.user.emails.find(email => email.primary).address,
                allowQuantity: false,
                passthrough: String(this.user.id),
                successCallback: () => this.updateSubscriptionInfo()
            })
        }
    }
}
