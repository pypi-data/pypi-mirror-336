import {postJson} from "../common"

import {PaymentPage} from "./page"
import {PricingPage} from "./pricing"

export class PaymentApp {
    constructor(app) {
        this.app = app
    }

    init() {
        this.app.routes["payment"] = {
            requireLogin: true,
            open: () => new PaymentPage(this.app.config)
        }
        this.app.routes["pricing"] = {
            open: () => new PricingPage(this.app.config)
        }

        this.app.getPaddleInfo = () => {
            if (this.app.paddleInfo) {
                return Promise.resolve()
            }
            return new Promise(resolve => {
                const paddleScript = document.createElement("script")
                paddleScript.onload = () => {
                    resolve()
                }
                document.head.appendChild(paddleScript)
                paddleScript.src = "https://cdn.paddle.com/paddle/paddle.js"
            })
                .then(() => postJson("/api/payment/get_paddle_info/"))
                .then(({json}) => {
                    const monthlyPlanId = json["monthly_plan_id"],
                        sixMonthsPlanId = json["six_months_plan_id"],
                        annualPlanId = json["annual_plan_id"],
                        vendorId = json["vendor_id"]
                    if (json["sandbox"]) {
                        window.Paddle.Environment.set("sandbox")
                    }
                    window.Paddle.Setup({
                        vendor: vendorId
                    })
                    return Promise.all([
                        new Promise(resolve =>
                            window.Paddle.Product.Prices(
                                monthlyPlanId,
                                response =>
                                    resolve({
                                        id: monthlyPlanId,
                                        price: response.recurring.price.gross,
                                        trial: response.recurring.subscription
                                            .trial_days
                                    })
                            )
                        ),
                        new Promise(resolve =>
                            window.Paddle.Product.Prices(
                                sixMonthsPlanId,
                                response =>
                                    resolve({
                                        id: sixMonthsPlanId,
                                        price: response.recurring.price.gross,
                                        trial: response.recurring.subscription
                                            .trial_days
                                    })
                            )
                        ),
                        new Promise(resolve =>
                            window.Paddle.Product.Prices(
                                annualPlanId,
                                response =>
                                    resolve({
                                        id: annualPlanId,
                                        price: response.recurring.price.gross,
                                        trial: response.recurring.subscription
                                            .trial_days
                                    })
                            )
                        )
                    ]).then(([monthly, sixmonths, annual]) => {
                        this.app.paddleInfo = {
                            vendorId,
                            monthly,
                            sixmonths,
                            annual
                        }
                        return Promise.resolve()
                    })
                })
        }

        this.app.getSubscription = () => {
            if (this.app.subscription) {
                return Promise.resolve()
            }
            return this.app
                .getPaddleInfo()
                .then(() => postJson("/api/payment/get_subscription_details/"))
                .then(({json}) => {
                    this.app.subscription = json
                    return Promise.resolve()
                })
        }
    }
}
