(* ::Package:: *)
(*
    checks.wl — print-before-assert check helpers for derivation stages.

    Load with:
        Get[FileNameJoin[{Environment["PROJECT_ROOT"], "symbolic", "common", "checks.wl"}]]

    Semantics, identical across checks.wl / checks.py / checks.jl:
      - a check PRINTS what it found, and THEN asserts it;
      - every check carries a short, stable, quoted label that a write-up cites;
      - ReportChecks[] prints a labelled tally and exits non-zero if anything failed.

    Print-before-assert is not decoration. A check that asserts without ever printing what it
    found is how a false PASS survives a whole session — see docs/failure_modes.md entry 1,
    where an assertion had been written to match the expectation and never compared to
    anything.
*)

BeginPackage["Checks`"];

CheckZero::usage      = "CheckZero[label, expr] prints expr and checks it is identically zero.";
CheckEqual::usage     = "CheckEqual[label, a, b] prints both and checks a === b after simplification.";
CheckTrue::usage      = "CheckTrue[label, cond] prints cond and checks it is True.";
CheckNumeric::usage   = "CheckNumeric[label, got, want, tol] prints both and checks |got-want| <= tol.";
ReportChecks::usage   = "ReportChecks[] prints the tally and Exit[1]s if any check failed.";

Begin["`Private`"];

$passed = 0; $failed = 0; $failures = {};

record[label_, ok_, shown_] := (
  Print[If[ok, "  [PASS] ", "  [FAIL] "], label, "  ->  ", shown];
  If[ok, $passed++, $failed++; AppendTo[$failures, label]];
  ok
);

CheckZero[label_String, expr_] := Module[{v = Simplify[expr]},
  (* print first: the printed value is the evidence, the assertion is the gate *)
  record[label, TrueQ[v === 0 || PossibleZeroQ[v]], v]];

CheckEqual[label_String, a_, b_] := Module[{d = Simplify[a - b]},
  record[label, TrueQ[d === 0 || PossibleZeroQ[d]], Row[{a, " vs ", b, "  difference: ", d}]]];

CheckTrue[label_String, cond_] := Module[{v = Simplify[cond]},
  record[label, TrueQ[v], v]];

CheckNumeric[label_String, got_, want_, tol_: 10^-10] := Module[{d = Abs[N[got - want]]},
  record[label, TrueQ[d <= tol], Row[{got, " vs ", want, "  |diff|: ", d, " tol: ", tol}]]];

ReportChecks[] := (
  Print["--- checks: ", $passed, " passed, ", $failed, " failed"];
  If[$failed > 0,
    Print["--- failed labels: ", $failures];
    Exit[1]];
  $passed);

End[];
EndPackage[];
