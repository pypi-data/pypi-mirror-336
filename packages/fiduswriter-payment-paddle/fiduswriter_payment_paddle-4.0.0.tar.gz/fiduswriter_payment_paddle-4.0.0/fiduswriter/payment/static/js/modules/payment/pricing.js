import {ensureCSS} from "../common"
import {advertisementTemplate} from "./templates"

import {PreloginPage} from "../prelogin"

export class PricingPage extends PreloginPage {
    constructor(config) {
        super(config)
        this.title = gettext("Pricing")
    }

    init() {
        ensureCSS([staticUrl("css/payment.css")])
        return this.app.getPaddleInfo().then(() => {
            this.contents = advertisementTemplate(
                Object.assign({infoOnly: true}, this.app.paddleInfo)
            )
            return super.init()
        })
    }
}
