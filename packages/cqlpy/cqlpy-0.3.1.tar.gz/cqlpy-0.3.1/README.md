# CQLpy

CQLpy is a Python implementation of the [Clinical Quality Language (CQL)](http://cql.hl7.org/). It is intended to be a complete implementation of the CQL specification and is currently in development.

See [CONTRIBUTING.md](CONTRIBUTING.md) for information on contributing to this project.

## Installation

```bash
pip install cqlpy
```

## Usage

```python
from cqlpy.context import Context
from cqlpy.providers import RosettaValuesetProvider

rosetta = RosettaValuesetProvider("<api-key>")
context = Context(rosetta, bundle_file_name="./fhir-bundle.json")

office_visit_valueset = ValueSet("http://cts.nlm.nih.gov/fhir/ValueSet/2.16.840.1.113883.3.464.1003.101.12.1001")
office_visits = context["Encounter", office_visit_valueset, "type"]
```

See [cqlpy_syntax_basics](notebooks/cqlpy_syntax_basics.ipynb) for more examples.

## Specification Implementation

### 1. Types

- [x] 1.1. [Any](http://cql.hl7.org/N1/09-b-cqlreference.html#any)
- [x] 1.2. [Boolean](http://cql.hl7.org/N1/09-b-cqlreference.html#boolean-1)
- [x] 1.3. [Code](http://cql.hl7.org/N1/09-b-cqlreference.html#code-1)
- [x] 1.4. [CodeSystem](http://cql.hl7.org/N1/09-b-cqlreference.html#codesystem)
- [x] 1.5. [Concept](http://cql.hl7.org/N1/09-b-cqlreference.html#concept-1)
- [x] 1.6. [Date](http://cql.hl7.org/N1/09-b-cqlreference.html#date)
- [x] 1.7. [DateTime](http://cql.hl7.org/N1/09-b-cqlreference.html#datetime)
- [x] 1.8. [Decimal](http://cql.hl7.org/N1/09-b-cqlreference.html#decimal-1)
- [x] 1.9. [Long](http://cql.hl7.org/N1/09-b-cqlreference.html#long-1)
- [x] 1.10. [Integer](http://cql.hl7.org/N1/09-b-cqlreference.html#integer-1)
- [x] 1.11. [Quantity](http://cql.hl7.org/N1/09-b-cqlreference.html#quantity)
- [ ] 1.12. [Ratio](http://cql.hl7.org/N1/09-b-cqlreference.html#ratio)
- [x] 1.13. [String](http://cql.hl7.org/N1/09-b-cqlreference.html#string-1)
- [ ] 1.14. [Time](http://cql.hl7.org/N1/09-b-cqlreference.html#time)
- [x] 1.15. [ValueSet](http://cql.hl7.org/N1/09-b-cqlreference.html#valueset)
- [ ] 1.16. [Vocabulary](http://cql.hl7.org/N1/09-b-cqlreference.html#vocabulary)

### 2. Logical Operators

- [ ] 2.1. [And](http://cql.hl7.org/N1/09-b-cqlreference.html#and)
- [ ] 2.2. [Implies](http://cql.hl7.org/N1/09-b-cqlreference.html#implies)
- [ ] 2.3. [Not](http://cql.hl7.org/N1/09-b-cqlreference.html#not)
- [ ] 2.4. [Or](http://cql.hl7.org/N1/09-b-cqlreference.html#or)
- [ ] 2.5. [Xor](http://cql.hl7.org/N1/09-b-cqlreference.html#xor)

### 3. Type Operators

- [ ] 3.1. [As](http://cql.hl7.org/N1/09-b-cqlreference.html#as)
- [ ] 3.2. [Children](http://cql.hl7.org/N1/09-b-cqlreference.html#children)
- [ ] 3.3. [Convert](http://cql.hl7.org/N1/09-b-cqlreference.html#convert)
- [ ] 3.4. [Descendents](http://cql.hl7.org/N1/09-b-cqlreference.html#descendents)
- [ ] 3.5. [Is](http://cql.hl7.org/N1/09-b-cqlreference.html#is)
- [ ] 3.6. [CanConvertQuantity](http://cql.hl7.org/N1/09-b-cqlreference.html#canconvertquantity)
- [ ] 3.7. [ConvertQuantity](http://cql.hl7.org/N1/09-b-cqlreference.html#convertquantity)
- [ ] 3.8. [ConvertsToBoolean](http://cql.hl7.org/N1/09-b-cqlreference.html#convertstoboolean)
- [ ] 3.9. [ConvertsToDate](http://cql.hl7.org/N1/09-b-cqlreference.html#convertstodate)
- [ ] 3.10. [ConvertsToDateTime](http://cql.hl7.org/N1/09-b-cqlreference.html#convertstodatetime)
- [ ] 3.11. [ConvertsToDecimal](http://cql.hl7.org/N1/09-b-cqlreference.html#convertstodecimal)
- [ ] 3.12. [ConvertsToLong](http://cql.hl7.org/N1/09-b-cqlreference.html#convertstolong)
- [ ] 3.13. [ConvertsToInteger](http://cql.hl7.org/N1/09-b-cqlreference.html#convertstointeger)
- [ ] 3.14. [ConvertsToQuantity](http://cql.hl7.org/N1/09-b-cqlreference.html#convertstoquantity)
- [ ] 3.15. [ConvertsToString](http://cql.hl7.org/N1/09-b-cqlreference.html#convertstostring)
- [ ] 3.16. [ConvertsToTime](http://cql.hl7.org/N1/09-b-cqlreference.html#convertstotime)
- [ ] 3.17. [ToBoolean](http://cql.hl7.org/N1/09-b-cqlreference.html#toboolean)
- [x] 3.18. [ToConcept](http://cql.hl7.org/N1/09-b-cqlreference.html#toconcept)
- [ ] 3.19. [ToDate](http://cql.hl7.org/N1/09-b-cqlreference.html#todate)
- [x] 3.20. [ToDateTime](http://cql.hl7.org/N1/09-b-cqlreference.html#todatetime)
- [ ] 3.21. [ToDecimal](http://cql.hl7.org/N1/09-b-cqlreference.html#todecimal)
- [ ] 3.22. [ToLong](http://cql.hl7.org/N1/09-b-cqlreference.html#tolong)
- [ ] 3.23. [ToInteger](http://cql.hl7.org/N1/09-b-cqlreference.html#tointeger)
- [ ] 3.24. [ToQuantity](http://cql.hl7.org/N1/09-b-cqlreference.html#toquantity)
- [ ] 3.25. [ToString](http://cql.hl7.org/N1/09-b-cqlreference.html#tostring)
- [ ] 3.26. [ToTime](http://cql.hl7.org/N1/09-b-cqlreference.html#totime)

### 4. Nullological Operators

- [x] 4.1. [Coalesce](http://cql.hl7.org/N1/09-b-cqlreference.html#coalesce)
- [x] 4.2. [IsNull](http://cql.hl7.org/N1/09-b-cqlreference.html#isnull)
- [x] 4.3. [IsFalse](http://cql.hl7.org/N1/09-b-cqlreference.html#isfalse)
- [x] 4.4. [IsTrue](http://cql.hl7.org/N1/09-b-cqlreference.html#istrue)

### 5. Comparison Operators

- [ ] 5.1. [Between](http://cql.hl7.org/N1/09-b-cqlreference.html#between)
- [x] 5.2. [Equal](http://cql.hl7.org/N1/09-b-cqlreference.html#equal)
- [x] 5.3. [Equivalent](http://cql.hl7.org/N1/09-b-cqlreference.html#equivalent)
- [x] 5.4. [Greater](http://cql.hl7.org/N1/09-b-cqlreference.html#greater)
- [x] 5.5. [Greater Or Equal](http://cql.hl7.org/N1/09-b-cqlreference.html#greater-or-equal)
- [x] 5.6. [Less](http://cql.hl7.org/N1/09-b-cqlreference.html#less)
- [x] 5.7. [Less Or Equal](http://cql.hl7.org/N1/09-b-cqlreference.html#less-or-equal)
- [x] 5.8. [Not Equal](http://cql.hl7.org/N1/09-b-cqlreference.html#not-equal)
- [ ] 5.9. [Not Equivalent](http://cql.hl7.org/N1/09-b-cqlreference.html#not-equivalent)

### 6. Arithmetic Operators

- [ ] 6.1. [Abs](http://cql.hl7.org/N1/09-b-cqlreference.html#abs)
- [ ] 6.2. [Add](http://cql.hl7.org/N1/09-b-cqlreference.html#add)
- [ ] 6.3. [Ceiling](http://cql.hl7.org/N1/09-b-cqlreference.html#ceiling)
- [ ] 6.4. [Divide](http://cql.hl7.org/N1/09-b-cqlreference.html#divide)
- [ ] 6.5. [Floor](http://cql.hl7.org/N1/09-b-cqlreference.html#floor)
- [ ] 6.6. [Exp](http://cql.hl7.org/N1/09-b-cqlreference.html#exp)
- [ ] 6.7. [HighBoundary](http://cql.hl7.org/N1/09-b-cqlreference.html#highboundary)
- [ ] 6.8. [Log](http://cql.hl7.org/N1/09-b-cqlreference.html#log)
- [ ] 6.9. [LowBoundary](http://cql.hl7.org/N1/09-b-cqlreference.html#lowboundary)
- [ ] 6.10. [Ln](http://cql.hl7.org/N1/09-b-cqlreference.html#ln)
- [x] 6.11. [Maximum](http://cql.hl7.org/N1/09-b-cqlreference.html#maximum)
- [x] 6.12. [Minimum](http://cql.hl7.org/N1/09-b-cqlreference.html#minimum)
- [ ] 6.13. [Modulo](http://cql.hl7.org/N1/09-b-cqlreference.html#modulo)
- [ ] 6.14. [Multiply](http://cql.hl7.org/N1/09-b-cqlreference.html#multiply)
- [ ] 6.15. [Negate](http://cql.hl7.org/N1/09-b-cqlreference.html#negate)
- [ ] 6.16. [Precision](http://cql.hl7.org/N1/09-b-cqlreference.html#precision)
- [ ] 6.17. [Predecessor](http://cql.hl7.org/N1/09-b-cqlreference.html#predecessor)
- [ ] 6.18. [Power](http://cql.hl7.org/N1/09-b-cqlreference.html#power)
- [ ] 6.19. [Round](http://cql.hl7.org/N1/09-b-cqlreference.html#round)
- [ ] 6.20. [Subtract](http://cql.hl7.org/N1/09-b-cqlreference.html#subtract)
- [ ] 6.21. [Successor](http://cql.hl7.org/N1/09-b-cqlreference.html#successor)
- [ ] 6.22. [Truncate](http://cql.hl7.org/N1/09-b-cqlreference.html#truncate)
- [ ] 6.23. [Truncated Divide](http://cql.hl7.org/N1/09-b-cqlreference.html#truncated-divide)

### 7. String Operators

- [ ] 7.1. [Combine](http://cql.hl7.org/N1/09-b-cqlreference.html#combine)
- [ ] 7.2. [Concatenate](http://cql.hl7.org/N1/09-b-cqlreference.html#concatenate)
- [x] 7.3. [EndsWith](http://cql.hl7.org/N1/09-b-cqlreference.html#endswith)
- [ ] 7.4. [Indexer](http://cql.hl7.org/N1/09-b-cqlreference.html#indexer)
- [ ] 7.5. [LastPositionOf](http://cql.hl7.org/N1/09-b-cqlreference.html#lastpositionof)
- [ ] 7.6. [Length](http://cql.hl7.org/N1/09-b-cqlreference.html#length)
- [ ] 7.7. [Lower](http://cql.hl7.org/N1/09-b-cqlreference.html#lower)
- [ ] 7.8. [Matches](http://cql.hl7.org/N1/09-b-cqlreference.html#matches)
- [ ] 7.9. [PositionOf](http://cql.hl7.org/N1/09-b-cqlreference.html#positionof)
- [ ] 7.10. [ReplaceMatches](http://cql.hl7.org/N1/09-b-cqlreference.html#replacematches)
- [x] 7.11. [Split](http://cql.hl7.org/N1/09-b-cqlreference.html#split)
- [ ] 7.12. [SplitOnMatches](http://cql.hl7.org/N1/09-b-cqlreference.html#splitonmatches)
- [ ] 7.13. [StartsWith](http://cql.hl7.org/N1/09-b-cqlreference.html#startswith)
- [ ] 7.14. [Substring](http://cql.hl7.org/N1/09-b-cqlreference.html#substring)
- [ ] 7.15. [Upper](http://cql.hl7.org/N1/09-b-cqlreference.html#upper)

### 8. Date and Time Operators

- [x] 8.1. [Add](http://cql.hl7.org/N1/09-b-cqlreference.html#add-1)
- [x] 8.2. [After](http://cql.hl7.org/N1/09-b-cqlreference.html#after)
- [x] 8.3. [Before](http://cql.hl7.org/N1/09-b-cqlreference.html#before)
- [x] 8.4. [Date](http://cql.hl7.org/N1/09-b-cqlreference.html#date-1)
- [x] 8.5. [DateTime](http://cql.hl7.org/N1/09-b-cqlreference.html#datetime-1)
- [ ] 8.6. [Date and Time Component From](http://cql.hl7.org/N1/09-b-cqlreference.html#datetime-component-from)
- [x] 8.7. [Difference](http://cql.hl7.org/N1/09-b-cqlreference.html#difference)
- [x] 8.8. [Duration](http://cql.hl7.org/N1/09-b-cqlreference.html#duration)
- [ ] 8.9. [Now](http://cql.hl7.org/N1/09-b-cqlreference.html#now)
- [ ] 8.10. [On Or After](http://cql.hl7.org/N1/09-b-cqlreference.html#on-or-after-1)
- [ ] 8.11. [On Or Before](http://cql.hl7.org/N1/09-b-cqlreference.html#on-or-before-1)
- [ ] 8.12. [Same As](http://cql.hl7.org/N1/09-b-cqlreference.html#same-as-1)
- [ ] 8.13. [Same Or After](http://cql.hl7.org/N1/09-b-cqlreference.html#same-or-after-1)
- [x] 8.14. [Same Or Before](http://cql.hl7.org/N1/09-b-cqlreference.html#same-or-before-1)
- [x] 8.15. [Subtract](http://cql.hl7.org/N1/09-b-cqlreference.html#subtract-1)
- [ ] 8.16. [Time](http://cql.hl7.org/N1/09-b-cqlreference.html#time-1)
- [ ] 8.17. [TimeOfDay](http://cql.hl7.org/N1/09-b-cqlreference.html#timeofday)
- [ ] 8.18. [Today](http://cql.hl7.org/N1/09-b-cqlreference.html#today)

### 9. Interval Operators

- [ ] 9.1. [After](http://cql.hl7.org/N1/09-b-cqlreference.html#after-1)
- [ ] 9.2. [Before](http://cql.hl7.org/N1/09-b-cqlreference.html#before-1)
- [x] 9.3. [Collapse](http://cql.hl7.org/N1/09-b-cqlreference.html#collapse)
- [ ] 9.4. [Contains](http://cql.hl7.org/N1/09-b-cqlreference.html#contains)
- [x] 9.5. [End](http://cql.hl7.org/N1/09-b-cqlreference.html#end)
- [ ] 9.6. [Ends](http://cql.hl7.org/N1/09-b-cqlreference.html#ends)
- [ ] 9.7. [Equal](http://cql.hl7.org/N1/09-b-cqlreference.html#equal-1)
- [ ] 9.8. [Equivalent](http://cql.hl7.org/N1/09-b-cqlreference.html#equivalent-1)
- [ ] 9.9. [Except](http://cql.hl7.org/N1/09-b-cqlreference.html#except)
- [ ] 9.10. [Expand](http://cql.hl7.org/N1/09-b-cqlreference.html#expand)
- [x] 9.11. [In](http://cql.hl7.org/N1/09-b-cqlreference.html#in)
- [ ] 9.12. [Includes](http://cql.hl7.org/N1/09-b-cqlreference.html#includes)
- [x] 9.13. [Included In](http://cql.hl7.org/N1/09-b-cqlreference.html#included-in)
- [ ] 9.14. [Intersect](http://cql.hl7.org/N1/09-b-cqlreference.html#intersect)
- [ ] 9.15. [Meets](http://cql.hl7.org/N1/09-b-cqlreference.html#meets)
- [ ] 9.16. [Not Equal](http://cql.hl7.org/N1/09-b-cqlreference.html#not-equal-1)
- [ ] 9.17. [Not Equivalent](http://cql.hl7.org/N1/09-b-cqlreference.html#not-equivalent-1)
- [ ] 9.18. [On Or After](http://cql.hl7.org/N1/09-b-cqlreference.html#on-or-after-2)
- [ ] 9.19. [On Or Before](http://cql.hl7.org/N1/09-b-cqlreference.html#on-or-before-2)
- [x] 9.20. [Overlaps](http://cql.hl7.org/N1/09-b-cqlreference.html#overlaps)
- [ ] 9.21. [Point From](http://cql.hl7.org/N1/09-b-cqlreference.html#point-from)
- [ ] 9.22. [Properly Includes](http://cql.hl7.org/N1/09-b-cqlreference.html#properly-includes)
- [ ] 9.23. [Properly Included In](http://cql.hl7.org/N1/09-b-cqlreference.html#properly-included-in)
- [ ] 9.24. [Same As](http://cql.hl7.org/N1/09-b-cqlreference.html#same-as-2)
- [ ] 9.25. [Same Or After](http://cql.hl7.org/N1/09-b-cqlreference.html#same-or-after-2)
- [ ] 9.26. [Same Or Before](http://cql.hl7.org/N1/09-b-cqlreference.html#same-or-before-2)
- [ ] 9.27. [Size](http://cql.hl7.org/N1/09-b-cqlreference.html#size)
- [x] 9.28. [Start](http://cql.hl7.org/N1/09-b-cqlreference.html#start)
- [ ] 9.29. [Starts](http://cql.hl7.org/N1/09-b-cqlreference.html#starts)
- [ ] 9.30. [Union](http://cql.hl7.org/N1/09-b-cqlreference.html#union)
- [ ] 9.31. [Width](http://cql.hl7.org/N1/09-b-cqlreference.html#width)

### 10. List Operators

- [ ] 10.1. [Contains](http://cql.hl7.org/N1/09-b-cqlreference.html#contains-1)
- [x] 10.2. [Distinct](http://cql.hl7.org/N1/09-b-cqlreference.html#distinct)
- [ ] 10.3. [Equal](http://cql.hl7.org/N1/09-b-cqlreference.html#equal-2)
- [ ] 10.4. [Equivalent](http://cql.hl7.org/N1/09-b-cqlreference.html#equivalent-2)
- [ ] 10.5. [Except](http://cql.hl7.org/N1/09-b-cqlreference.html#except-1)
- [x] 10.6. [Exists](http://cql.hl7.org/N1/09-b-cqlreference.html#exists)
- [x] 10.7. [Flatten](http://cql.hl7.org/N1/09-b-cqlreference.html#flatten)
- [x] 10.8. [First](http://cql.hl7.org/N1/09-b-cqlreference.html#first)
- [x] 10.9. [In](http://cql.hl7.org/N1/09-b-cqlreference.html#in-1)
- [ ] 10.10. [Includes](http://cql.hl7.org/N1/09-b-cqlreference.html#includes-1)
- [ ] 10.11. [Included In](http://cql.hl7.org/N1/09-b-cqlreference.html#included-in-1)
- [ ] 10.12. [Indexer](http://cql.hl7.org/N1/09-b-cqlreference.html#indexer-1)
- [ ] 10.13. [IndexOf](http://cql.hl7.org/N1/09-b-cqlreference.html#indexof)
- [ ] 10.14. [Intersect](http://cql.hl7.org/N1/09-b-cqlreference.html#intersect-1)
- [x] 10.15. [Last](http://cql.hl7.org/N1/09-b-cqlreference.html#last)
- [ ] 10.16. [Length](http://cql.hl7.org/N1/09-b-cqlreference.html#length-1)
- [ ] 10.17. [Not Equal](http://cql.hl7.org/N1/09-b-cqlreference.html#not-equal-2)
- [ ] 10.18. [Not Equivalent](http://cql.hl7.org/N1/09-b-cqlreference.html#not-equivalent-2)
- [ ] 10.19. [Properly Includes](http://cql.hl7.org/N1/09-b-cqlreference.html#properly-includes-1)
- [ ] 10.20. [Properly Included In](http://cql.hl7.org/N1/09-b-cqlreference.html#properly-included-in-1)
- [x] 10.21. [Singleton From](http://cql.hl7.org/N1/09-b-cqlreference.html#singleton-from)
- [ ] 10.22. [Skip](http://cql.hl7.org/N1/09-b-cqlreference.html#skip)
- [ ] 10.23. [Tail](http://cql.hl7.org/N1/09-b-cqlreference.html#tail)
- [ ] 10.24. [Take](http://cql.hl7.org/N1/09-b-cqlreference.html#take)
- [x] 10.25. [Union](http://cql.hl7.org/N1/09-b-cqlreference.html#union-1)

### 11. Aggregate Functions

- [ ] 11.1. [AllTrue](http://cql.hl7.org/N1/09-b-cqlreference.html#alltrue)
- [ ] 11.2. [AnyTrue](http://cql.hl7.org/N1/09-b-cqlreference.html#anytrue)
- [ ] 11.3. [Avg](http://cql.hl7.org/N1/09-b-cqlreference.html#avg)
- [x] 11.4. [Count](http://cql.hl7.org/N1/09-b-cqlreference.html#count)
- [ ] 11.5. [GeometricMean](http://cql.hl7.org/N1/09-b-cqlreference.html#geometricmean)
- [ ] 11.6. [Max](http://cql.hl7.org/N1/09-b-cqlreference.html#max)
- [ ] 11.7. [Min](http://cql.hl7.org/N1/09-b-cqlreference.html#min)
- [ ] 11.8. [Median](http://cql.hl7.org/N1/09-b-cqlreference.html#median)
- [ ] 11.9. [Mode](http://cql.hl7.org/N1/09-b-cqlreference.html#mode)
- [ ] 11.10. [Population StdDev](http://cql.hl7.org/N1/09-b-cqlreference.html#population-stddev)
- [ ] 11.11. [Population Variance](http://cql.hl7.org/N1/09-b-cqlreference.html#population-variance)
- [ ] 11.12. [Product](http://cql.hl7.org/N1/09-b-cqlreference.html#product)
- [ ] 11.13. [StdDev](http://cql.hl7.org/N1/09-b-cqlreference.html#stddev)
- [ ] 11.14. [Sum](http://cql.hl7.org/N1/09-b-cqlreference.html#sum)
- [ ] 11.15. [Variance](http://cql.hl7.org/N1/09-b-cqlreference.html#variance)

### 12. Clinical Operators

- [ ] 12.1. [Age](http://cql.hl7.org/N1/09-b-cqlreference.html#age)
- [ ] 12.2. [AgeAt](http://cql.hl7.org/N1/09-b-cqlreference.html#ageat)
- [ ] 12.3. [CalculateAge](http://cql.hl7.org/N1/09-b-cqlreference.html#calculateage)
- [x] 12.4. [CalculateAgeAt](http://cql.hl7.org/N1/09-b-cqlreference.html#calculateageat)
- [ ] 12.5. [Equal](http://cql.hl7.org/N1/09-b-cqlreference.html#equal-3)
- [ ] 12.6. [Equivalent](http://cql.hl7.org/N1/09-b-cqlreference.html#equivalent-3)
- [ ] 12.7. [In (Codesystem)](http://cql.hl7.org/N1/09-b-cqlreference.html#in-codesystem)
- [ ] 12.8. [ExpandValueSet (ValueSet)](http://cql.hl7.org/N1/09-b-cqlreference.html#expandvalueset)
- [x] 12.9. [In (Valueset)](http://cql.hl7.org/N1/09-b-cqlreference.html#in-valueset)

### 13. Errors and Messaging

- [ ] 13.1. [Message](http://cql.hl7.org/N1/09-b-cqlreference.html#message)
