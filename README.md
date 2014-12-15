# Thresh

Thresh is a crowdfunding platform under development which allows people to
make tangible offers of support for any number of proposals without incurring
additional obligations with each new offer they make.

**The code in this repository is an early prototype and not yet functional.**

## Vocabulary

* **Proposal**
 * A document soliciting offers toward a fixed amount of funding. Similar to a
   *project* or *campaign* on Kickstarter or Indiegogo.

* **Supporter**
 * A person who gives money to support proposals. Similar to a *funder* on
   Indiegogo or a *backer* on Kickstarter.

* **Offer**
 * A supporter's offer of support to a proposal, contingent upon the proposal
   reaching its funding goal. Similar to (but not the same as) a *pledge* on
   Kickstarter.

* **Intermediary**
 * The entity running the Thresh service.

## How it works

Supporters deposit funds with the intermediary. The deposited funds can be
offered to multiple proposals simultaneously. All offers to active proposals
exist in one of two states: *backed*, or *un-backed*. Backed offers are those
which can be fulfilled using funds that the supporter has deposited. All
offers must be backed when they are created.

The funds stored with the intermediary can be used to make backed offers to an
unlimited number of proposals.

Proposals are funded when the sum of their backed offers reaches their goal.

When a proposal is funded, it will usually cause some offers to other proposals
to become un-backed. These offers will expire after some period of time if the
supporter does not renew them with sufficient backing.

## Motivation

There are two primary reasons why this system is more desirable than existing
threshold pledge formuli:

### Funding long-term, ambitious, and/or crazy ideas

In the threshold pledge systems which are widely used today, making each pledge
of support requires that the supporter is able and willing to commit the amount
of money being pledged to each specific project for the duration of the
projects' funding periods. For this reason, campaigns must be limited to
relatively short funding periods (for example, a maximum of 60 days on
Kickstarter) and most supporters cannot afford to pledge support to a large
number of projects simultaneously.

While this model has successfully provided funding for many projects, its
necessarily short funding periods discourage ambitious or seemingly
unlikely-to-succeed ideas from being supported or even proposed. Our
expectation is that more ambitious proposals are achievable if they have enough
time to mature in the right environment, and people will be more willing to
support them if the barrier of taking on additional obligation with each
additional pledge is removed.

### Decision-making and task prioritization

A single project (in the colloquial meaning of the word, not the
Kickstarter/Indiegogo meaning) might make many proposals and let their
supporters choose which will be implemented next (or at all). For example,
supporters could decide which feature software developers should implement
next, or which songs a band should record in a studio next. In this type of
application, it could make sense for a project to run its own instance of
Thresh so that all of their proposals are only in "competition" with eachother
and not unrelated things.

## Example

1. Alice creates a proposal with a goal of $1,000

2. Bob creates a proposal with a goal of $100

3. Carol sends the intermediary $10 and uses it to make backed offers to both
   Alice and Bob's proposals. The two proposals now have $10 in backed offers
   each.

4. Other people make backed offers totaling $900 to Alice's project, giving it
   a total of $910 in backed offers.

5. Other people make backed offers totaling $90 to Bob's project, causing it to
   be funded. Carol's $10 is included in the $100 transferred from the
   intermediary to Bob.

At this point, Alice's proposal has returned to having only $900 in backed
offers, but it also has $10 in unbacked offers. Carol can decide to send
another $10 to renew the offer to Alice (as well as any other offers for $10 or
less which they've previously made to other proposals).

## FAQ

* Why would creators or supporters want to use this service?

  * Creators

    - might want to use Thresh if seems likely to enable them to reach funding
      goals which other platforms cannot.

    - might want to use Thresh to allow their supporters to help make decisions
      or prioritize tasks through a process similar to approval voting.

  * Supporters

    - might want to use Thresh because one or more proposal they want to
      support is using it to raise funds.

    - might want to use Thresh because it is fun and low-risk to offer support
      to seemingly-improbable proposals which couldn't be found on other sites.

  * Although not specific to Thresh's alternative threshold pledge model,
    creators and supporters both might prefer to use Thresh because it is
    self-hostable bitcoin-compatible free software which doesn't require anyone
    to use Amazon, PayPal, Facebook, or similar services.

* Competition between proposals sounds unpleasant.

 * Although it is possible to use Thresh to select one of a set of
   mutually-exclusive proposals, in most cases we expect the "competition" will
   not be win-or-lose. When one proposal is successful, it should only be a
   short-term setback for other proposals backed by some of the same supporters
   (because we expect that many supporters will choose to deposit more money to
   maintain their other offers of support).

* Is this a sort of multi-winner approval voting with money as votes?

 * Sort of, but not precisely: because proposals don't share (or even
   necessarily have) ending dates, today's "loser" might still eventually
   also win in the future.

* Is this a winner-takes-all version of Flattr?

 * Sort of, but not precisely: you could easily have a monthly automatic
   spend amount, but still contribute to the completion of many proposals
   each month (eg, if you make many offers that are smaller than the total
   amount you decide to spend each month). So it's more
   winners-take-their-offer than winner-take-all.

* When do proposals expire?

 * Creators may set whatever expiration date they think is appropriate, or let
   their proposal remain open indefinitely.

* When do offers expire?

 * Supporters may set an expiration date on each backed offer they make. If
   the proposal specifies an expiration date, that date is the maximum (and
   default) value.

 * Intermediaries define the expiration period of all unbacked offers. To
   facilitate the monthly automatic deposit usage pattern, the intermediary's
   chosen expiration period for un-backed offers should probably be one month
   or more.

* Is Thresh cheaper than other crowdfunding tools?

 * That's up to the operator of the service (the intermediary), but Thresh is
   designed to be operable as a free service.

* Do I have to use BTC (bitcoin)?

 * No. We are implementing Bitcoin first, but intend to have modular support
   for other currencies. You can use other forms of currency if you host your
   own instance of the software (be your own intermediary). You can even eschew
   traditional forms of currency and replace it with whatever you want...

* Why not allow proposals to accept offers in multiple currencies?

 * Because to have a single threshold for the proposal, the intermediary would
   need to provide a currency exchange service which would be complicated and
   either (a) not competitive with existing currency exchanges or (b) a fraud
   magnet. So, an intermediary can support as many currencies as they like, but
   each proposal can only accept offers in one currency.

* Why is the anonymity configured on a per-supporter-account basis instead of
  per-offer or per-proposal?

 * Because that is the only way to provide meaningful unlinkability. If a
   supporter were able to make some offers anonymously while being credited for
   other offers, their anonymous offers would be inferable when their success
   caused non-anonymous offers to become unbacked. So, if you want to support
   some things anonymously and other things not anonymously, you'll want (at
   least) two accounts.

* Forking and pull requests for proposals? What is this, a version controlled
  crowdfunding tool?

 * Yes. It's run off of Git, so you can fork proposals or commit changes to
   your own projects in order to arrive at a proposal that finds adequate
   support. Each revision is effectively a new proposal which automatically
   notifies supporters of its parent(s) so that they'll have the opportunity
   to offer to support it also or instead. Supporters can make offers to forks
   or pull requests, but offers to pull requests cannot be completed unless
   the original creator accepts it.

* Git? That's way too complicated, most people won't use it.

 * The goal is to use git under the hood for editable content like proposals,
   and make a git interface available to people who know what git is, but to
   also provide all functionality through a web interface that does not
   require knowing what git is. Editing proposal documents should be as easy as
   editing something on any other website.

* Is Thresh just for funding projects then?

 * Thresh is for funding proposals, or task prioritization of proposals by
   supporters.

* Will Thresh let supporters choose which rewards they receive? (This is
  apparently a frequently requested feature on Kickstarter.)

 * No. In fact, Thresh will not provide a means outside of the proposal text
   for suggesting specific offer amounts, or do anything to facilitate rewards
   at all. We're not building another ecommerce tool for selling or giving away
   physical goods, and certainly not for artificially scarce digital goods,
   as there are enough of those systems already. If creators are determined
   to provide rewards to their supporters, Thresh won't do anything to stop
   them but it also won't encourage that approach by specifically facilitating
   it. This is a funding model for the post-artificial-scarcity future. And
   truthfully, one of the goals is to beguile people into being
   philanthropists.


## Installation

TBD

## License

Thresh is copyright 2012-2014 by its authors (see file AUTHORS) and is licensed under [GNU GPL v3](https://gnu.org/licenses/gpl-3.0.txt) or any later release.



