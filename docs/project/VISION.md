# BrAPI-GenX Vision

An agricultural research question rarely fits inside one system. To understand
how two wheat cultivars performed under different irrigation regimes, a
researcher may need breeding records, trial design, soil measurements, weather
observations, irrigation logs, and harvest results. Each source can describe
its part well. The difficulty is connecting those records while preserving
what each one means.

Our vision is for independent agricultural systems to exchange enough
context that researchers can follow those connections and use the evidence.
**Agricultural Knowledge Fabric** is the working name for this broader idea.
Plant breeding is the starting point. The same approach can grow to connect
information from agronomy, plant health, land and water management, remote
sensing, livestock, aquaculture, and agrifood supply chains as concrete needs
emerge.

## BrAPI-GenX’s role

BrAPI-GenX starts from the official BrAPI v2.1 contracts for plant breeding.
It is an independently governed contribution with its own `/genx/v1/`
namespace for additive extensions. BrAPI-GenX preserves the published BrAPI
compatibility surface and uses established companion standards where they
already express the scientific meaning.

A proposal earns its place by showing where an exchange breaks down. A
documented failure, a reproducible example, or relevant research should show
what meaning an independent system cannot recover. Sometimes the answer is
to use an existing contract or make a mapping explicit. When a gap remains,
GenX should specify the smallest addition that lets independent systems
recover the missing meaning. See the [specification quality standard](../governance/BRAPI-GENX-SPECIFICATION-QUALITY-STANDARD.md).

## Scientific meaning across systems

Data can stay with the institutions and systems that maintain it. Shared
references allow a researcher to follow a record back to its source, resolve
which cultivar, plot, or study it describes, and identify the version used.
A measurement should carry the context needed to interpret it, including
where and when it was made, the method, the units, and the uncertainty where
known. A soil measurement needs its sampling depth. A weather value needs
its period and location. Grain yield needs a clear measurement basis.

The exchange should preserve the distinction between what was planned,
what was applied, what was measured, and what was calculated or predicted.
A weather forecast belongs in its meteorological context even when a crop
model consumes it. Shared computational methods can support several domains
while each domain retains authority over its own meaning.

## The first proof

Start with one wheat trial. Connect the germplasm and trial design to the
plot-level records, the relevant soil and weather context, the irrigation
actually applied, and the measured grain yield. An independent reader should
be able to follow those records across sources and explain why each piece of
evidence applies to a given plot and season. The demonstrator should also
show how an ambiguous link, missing measurement context, or unresolved
identifier appears to the reader.

The milestone is reached when independent systems can reconstruct the same
scientific record from the documented exchange. That gives us a concrete
basis for deciding which connections to generalize and where to extend next.

## Long-term research goal

As those connections grow, researchers and computational tools should be
able to discover datasets and analytical methods, reproduce results, and
ask questions that cross disciplinary boundaries. AI can use this
infrastructure to explore relationships and propose hypotheses. Each
hypothesis should remain identifiable as such, with a trace back to the
observations, methods, and assumptions that support it.

The contracts specify scientific meaning and observable behavior so that
different organizations can implement them in their own systems. BijMantra
can be one participant in that ecosystem. The value comes from independent
systems being able to exchange and verify the same evidence.
