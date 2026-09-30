#!/usr/bin/env wolframscript
(* ::Package:: *)
(*
    Topic:          <topic>
    Stage:          NN — <what this stage establishes, in one line>
    Owner tool:     Mathematica            (* the record for this topic; docs/toolchain.md *)
    Kind:           REPRODUCTION           (* | EXTENSION | CROSS-CHECK *)
    Judged against: <source Eq./Table N>   (* or: named benchmark / physics *)
    Inputs:         symbolic/<topic>/out/<NN-1>_<what>.m
    Outputs:        symbolic/<topic>/out/NN_<what>.m

    Run:            scripts/run symbolic/<topic>/stage_NN_<what>.wls
    Rules:          .claude/rules/derivation.md  (one stage per file; print before assert;
                    append-only; every check labelled)

    This file is a TEMPLATE. Copy it; do not edit it in place.
*)

root = Environment["PROJECT_ROOT"];
If[root === $Failed, Print["PROJECT_ROOT unset; run via scripts/run"]; Exit[1]];
Get[FileNameJoin[{root, "symbolic", "common", "checks.wl"}]];
(* checks.wl provides: CheckZero[label, expr], CheckEqual[label, a, b],
   CheckTrue[label, cond], ReportChecks[] — each PRINTS before asserting,
   and ReportChecks[] exits non-zero if any check failed. *)

Print["=== Stage NN: <what this stage establishes> ==="];

(* ---------------------------------------------------------------------------
   1. Inputs and assumptions. State every assumption where it is used.
   --------------------------------------------------------------------------- *)

prev = Get[FileNameJoin[{root, "symbolic", "<topic>", "out", "<NN-1>_<what>.m"}]];
assumptions = {r > 0, l >= 2};

(* ---------------------------------------------------------------------------
   2. The derivation. Print each intermediate result: a step nobody saw is a
      step nobody checked.
   --------------------------------------------------------------------------- *)

result = Simplify[ (* ... *) , Assumptions -> assumptions];
Print["result = ", result // InputForm];

(* ---------------------------------------------------------------------------
   3. Checks. One labelled check per non-trivial claim. Labels are cited by the
      write-up, so keep them short and stable — renaming one breaks a citation
      (make check-evidence).
   --------------------------------------------------------------------------- *)

CheckZero["back-substitution residual vanishes",
  Simplify[ (* original /. solution *) , Assumptions -> assumptions]];

CheckEqual["reduced system matches source Eq. (N), coefficient by coefficient",
  CoefficientList[derived, x], CoefficientList[sourceEq, x]];

CheckZero["reduces to the verified <special case> when <parameter> -> 0",
  Simplify[result /. q -> 0, Assumptions -> assumptions] - verifiedSpecialCase];

CheckTrue["scaling consistency", (* dimensional or scaling invariant *) True];

(* ---------------------------------------------------------------------------
   4. Persist as text. Never a version-specific binary format.
   --------------------------------------------------------------------------- *)

Put[result, FileNameJoin[{root, "symbolic", "<topic>", "out", "NN_<what>.m"}]];

ReportChecks[];   (* prints the pass/fail tally and Exit[1]s on any failure *)
