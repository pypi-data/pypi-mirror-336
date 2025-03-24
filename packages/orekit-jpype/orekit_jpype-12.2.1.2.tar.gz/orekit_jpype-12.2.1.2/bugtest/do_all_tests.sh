for file in *Test.py
    echo "Running tests while ignoring $file"
    uv run python -m pytest --ignore "$file" > "log_$file.txt" 2>&1
    if test $status -eq 139
        echo "SIGSEGV occurred when ignoring $file. See log_$file.txt for details."
    else
        echo "No SIGSEGV when ignoring $file."
    end
end


set all_files (ls *Test.py)
for file in $all_files
    set ignore_args
    for other in $all_files
        if test "$other" != "$file"
            set ignore_args $ignore_args --ignore "$other"
        end
    end
    echo "Running tests for $file only"
    uv run python -m pytest $ignore_args > "log_$file.txt" 2>&1
    if test $status -eq 139
        echo "SIGSEGV occurred when running $file. See log_$file.txt for details."
    else
        echo "No SIGSEGV when running $file."
    end
end

####

# Define Group 1 files explicitly (adjust if needed)
set group1_files AltitudeDetectorTest.py BackAndForthDetectorTest.py BrouwerLyddanePropagatorTest.py EphemerisEventsTest.py EventDetectorTest.py EventHandlerTest.py FieldStopOnDecreasingTest.py FixedPointTleGenerationAlgorithmTest.py GroundFieldOfViewDetectorTest.py HaloOrbitTest.py ImpulseManeuverTest.py InterSatDirectViewDetectorTest.py IodGibbsTest.py IodLaplaceTest.py

set count (count $group1_files)
set half (math "($count + 1) / 2")

set subgroup1 $group1_files[1..$half]
set subgroup2 $group1_files[(math "$half + 1")..$count]

echo "Running subgroup1 (first half of Group 1):"
uv run python -m pytest $subgroup1 > log_subgroup1.txt 2>&1
if test $status -eq 139
    echo "SIGSEGV occurred in subgroup1. See log_subgroup1.txt for details."
else
    echo "No SIGSEGV in subgroup1."
end

echo "Running subgroup2 (second half of Group 1):"
uv run python -m pytest $subgroup2 > log_subgroup2.txt 2>&1
if test $status -eq 139
    echo "SIGSEGV occurred in subgroup2. See log_subgroup2.txt for details."
else
    echo "No SIGSEGV in subgroup2."
end


###

Subgroup2: FixedPointTleGenerationAlgorithmTest.py GroundFieldOfViewDetectorTest.py HaloOrbitTest.py ImpulseManeuverTest.py InterSatDirectViewDetectorTest.py IodGibbsTest.py IodLaplaceTest.py
Running subgroup1 (first half of Group 1):
No SIGSEGV in subgroup1.
Running subgroup2 (second half of Group 1):


####

# Define subgroup2 files explicitly.
set subgroup2_files FixedPointTleGenerationAlgorithmTest.py GroundFieldOfViewDetectorTest.py HaloOrbitTest.py ImpulseManeuverTest.py InterSatDirectViewDetectorTest.py IodGibbsTest.py IodLaplaceTest.py

# Count subgroup2 files and split them into two smaller groups.
set count (count $subgroup2_files)
set half (math "($count + 1) / 2" | string replace -r '\..*' '')
set start2 (math "$half + 1" | string replace -r '\..*' '')

set sub2a $subgroup2_files[1..$half]
set sub2b $subgroup2_files[$start2..$count]

echo "Running subgroup2a (first half of subgroup2) ($sub2a):"
uv run python -m pytest $sub2a > log_subgroup2a.txt 2>&1
if test $status -eq 139
    echo "SIGSEGV occurred in subgroup2a. See log_subgroup2a.txt for details."
else
    echo "No SIGSEGV in subgroup2a."
end

echo "Running subgroup2b (second half of subgroup2) ($sub2b):"
uv run python -m pytest $sub2b > log_subgroup2b.txt 2>&1
if test $status -eq 139
    echo "SIGSEGV occurred in subgroup2b. See log_subgroup2b.txt for details."
else
    echo "No SIGSEGV in subgroup2b."
end


### IodLaplaceTest.py failing! HaloOrbit as well


