export const advertisementTemplate = ({
    subscribed,
    monthly,
    sixmonths,
    annual,
    subscription_end,
    infoOnly = false
}) => `
<div class="pricing-guide${infoOnly ? " info-only" : ""}">
    <h1>${gettext("Pricing Guide")}</h1>
    <p>
        ${gettext("You can write 2 documents on the Free Plan without any trial period.")}
        <br>
        ${gettext("If you want to write more documents, you can upgrade your plan below.")}
    </p>
    <div class="price-boxes">
        <div class="price-box">
            <h3>${gettext("Basic")}</h3>
            <h2>${gettext("Free Plan")}</h2>
            <ul class="fa-ul">
                <li><i class="fa-li fa fa-check"></i>${gettext("2 free documents")}</li>
                <li><i class="fa-li fa fa-check"></i>${gettext("Unlimited collaborators")}</li>
                <li><i class="fa-li fa fa-check"></i>${gettext("Unlimited bibliography items")}</li>
                <li><i class="fa-li fa fa-check"></i>${gettext("Unlimited exports")}</li>
            </ul>
            <div class="price-offer">
                <button${subscribed && !subscription_end ? ' class="subscription"' : ""}>
                ${
                    infoOnly
                        ? gettext("Default")
                        : subscribed
                          ? subscription_end
                              ? gettext("Downgrade on ") + subscription_end
                              : gettext("Default")
                          : gettext("Current")
                }
                </button>
            </div>
        </div>
        <div class="price-box upgrade">
            <h3>${gettext("Premium")}</h3>
            <h2>${gettext("Paid Plan")}</h2>
            <ul class="fa-ul">
                <li><i class="fa-li fa fa-check"></i><strong>${gettext("Unlimited documents")}</strong></li>
                <li><i class="fa-li fa fa-check"></i>${gettext("Unlimited collaborators")}</li>
                <li><i class="fa-li fa fa-check"></i>${gettext("Unlimited bibliography items")}</li>
                <li><i class="fa-li fa fa-check"></i>${gettext("Unlimited exports")}</li>
            </ul>
            <div class="price-offer">
                <p><strong>${gettext("Monthly payments")}</strong></p>
                <button class="subscription monthly${subscribed === "monthly" ? " current" : ""}">
                    ${
                        infoOnly
                            ? ""
                            : `${
                                  subscribed === "monthly"
                                      ? subscription_end
                                          ? gettext("Resubscribe")
                                          : gettext("Modify")
                                      : !subscribed
                                        ? gettext("Sign up")
                                        : gettext("Switch")
                              }: `
                    }
                    ${monthly.price}
                </button>
                ${monthly.trial ? `<div>${gettext("Trial")}: ${monthly.trial} ${gettext("days")}</div>` : ""}
            </div>
            <div class="price-offer">
                <p><strong>${gettext("Semiannual payments")}</strong></p>
                <button class="subscription sixmonths${subscribed === "sixmonths" ? " current" : ""}">
                    ${
                        infoOnly
                            ? ""
                            : `${
                                  subscribed === "sixmonths"
                                      ? subscription_end
                                          ? gettext("Resubscribe")
                                          : gettext("Modify")
                                      : !subscribed
                                        ? gettext("Sign up")
                                        : gettext("Switch")
                              }: `
                    }
                    ${sixmonths.price}
                </button>
                ${sixmonths.trial ? `<div>${gettext("Trial")}: ${sixmonths.trial} ${gettext("days")}</div>` : ""}
            </div>
            <div class="price-offer">
                <p><strong>${gettext("Annual payments")}</strong></p>
                <button class="subscription annual${subscribed === "annual" ? " current" : ""}">
                    ${
                        infoOnly
                            ? ""
                            : `${
                                  subscribed === "annual"
                                      ? subscription_end
                                          ? gettext("Resubscribe")
                                          : gettext("Modify")
                                      : !subscribed
                                        ? gettext("Sign up")
                                        : gettext("Switch")
                              }: `
                    }
                    ${annual.price}
                </button>
                ${annual.trial ? `<div>${gettext("Trial")}: ${annual.trial} ${gettext("days")}</div>` : ""}
            </div>
        </div>
    </div>
    <p><strong>${gettext("Refunds and cancellation")}</strong>: ${gettext("Subscriptions can be cancelled at any time. If a cancellation took place during the trial period, no charge will be made. Thereafter, subscriptions are charged in advance and no refunds will be made.")}
    ${gettext("See")} <a href="/pages/terms/">${gettext("Terms and Conditions")}</a>.</p>
    <p>${gettext("Our order process is conducted by our online reseller Paddle.com. Paddle.com is the Merchant of Record for all our orders. Paddle provides all customer service inquiries and handles returns.")}</p>
</div>`
