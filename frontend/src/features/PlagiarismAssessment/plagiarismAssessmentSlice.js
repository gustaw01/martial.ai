import { createSelector, createEntityAdapter } from "@reduxjs/toolkit";
import { apiSlice } from "../../app/api/apiSlice";

const plagiarismAssessmentAdapter = createEntityAdapter();

const initialState = plagiarismAssessmentAdapter.getInitialState();

export const plagiarismAssessmentApiSlice = apiSlice.injectEndpoints({
    endpoints: (builder) => ({
        getPlagiarismAssessment: builder.query({
            query: () => '/plagiarism_assessment',
            transformResponse: (responseData) =>
                plagiarismAssessmentAdapter.setAll(initialState, responseData),
            providesTags: (result, error, arg) =>
                result
                    ? [
                        { type: 'PlagiarismAssessment', id: "LIST" },
                        ...result.ids.map((id) => ({ type: 'PlagiarismAssessment', id })),
                    ]
                    : [{ type: 'PlagiarismAssessment', id: "LIST" }],
        }),
        addNewPlagiarismAssessment: builder.mutation({
            query: (newPlagiarismAssessment) => {
                const isFormData = newPlagiarismAssessment instanceof FormData;
                return {
                    url: '/plagiarism_assessment',
                    method: 'POST',
                    body: newPlagiarismAssessment,
                    headers: isFormData ? undefined : { 'Content-Type': 'application/json' },
                };
            },
            invalidatesTags: [{ type: 'PlagiarismAssessment', id: "LIST" }],
        }),
    })
});

export const {
    useGetPlagiarismAssessmentQuery,
    useAddNewPlagiarismAssessmentMutation,
} = plagiarismAssessmentApiSlice;

export const selectPlagiarismAssessmentResult = plagiarismAssessmentApiSlice.endpoints.getPlagiarismAssessment.select();

const selectPlagiarismAssessmentData = createSelector(
    selectPlagiarismAssessmentResult,
    (plagiarismAssessmentResult) => plagiarismAssessmentResult.data ?? initialState
)

export const {
    selectAll: selectAllPlagiarismAssessment,
    selectById: selectPlagiarismAssessmentById,
    selectIds: selectPlagiarismAssessmentIds
} = plagiarismAssessmentAdapter.getSelectors(
    (state) => selectPlagiarismAssessmentData(state)
);